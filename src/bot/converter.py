import os
from src.bot.convert_tools import *
from time import time
from src.bot.logger import Logger
from pathlib import Path
from src.bot.util import os_path, get_desired_resolution

buf_filename = lambda counter, step: f"buf-{counter}-{step}.mp4"
out_filename = lambda counter: f"out-{counter}.webm"

def get_resolution_from_str(res):
    res_arr = res.split("x")
    return list(map(int, res_arr))

class PipeModes:
    Crop = 0
    CropAndSpeedup = 1
    Speedup = 2
    modes_list = [0, 1, 2]

class Converter:
    def __init__(self, in_folder, buf_folder, out_folder, logger=None):
        self.to_process = []
        self.counter = 0
        self.logger: Logger = logger
        self.in_f = in_folder
        self.buf_f = buf_folder
        self.out_f = out_folder
        self.clear_folder(self.buf_f)
        self.clear_folder(self.out_f)
    
    def create_and_run_pipe(self, filename, mode = None):
        pipeline = ProcessPipeline(filename, self.counter, self.in_f, self.buf_f, self.out_f)
        if mode is not None:
            pipeline.set_pipe_mode(mode)
        pipeline.setup_pipe()
        pipeline.run()
        os.remove(os_path(f"{self.in_f}/{filename}"))
        self.clear_folder(self.buf_f)
        self.counter += 1
        return os_path(f"{self.out_f}/{out_filename(self.counter - 1)}")
    
    def clear_folder(self, folder):
        for file in os.listdir(folder):
            os.remove(os_path(f"{folder}/{file}"))
    
class ProcessPipeline:
    def __init__(self, filename, index, in_f="", buf_f="", out_f="") -> None:
        self.filename = filename
        self.index = index
        self.in_f = in_f
        self.buf_f = buf_f
        self.out_f = out_f
        self.pipe = []
        self.mode = PipeModes.Crop
        self.step = 0
    
    def set_pipe_mode(self, mode):
        self.mode = mode
    
    def setup_pipe(self):
        v_length = float(run_command(video_length(self.last_filename())).replace("\n", "")) # video length in seconds
        v_res = get_resolution_from_str(run_command(video_resolution(self.last_filename()))) # video resolution

        match self.mode:
            case PipeModes.Crop:
                self.pipe += self.pipe_crop(v_length, v_res)
            case PipeModes.CropAndSpeedup:
                self.pipe += self.pipe_crop_speedup(v_length, v_res)
            case PipeModes.Speedup:
                self.pipe += self.pipe_speedup(v_length, v_res)
        # then, based on the user choice, create a pipeline

        self.pipe.append(mp4_to_webm(
            self.last_filename(),
            f"{self.out_f}/{out_filename(self.index)}"
        )) # convert and create a final file
    
    def run(self):
        for command in self.pipe:
            run_command(command, record_time=True)

    def last_filename(self):
        if self.step == 0:
            return os_path(f"{self.in_f}/{self.filename}")
        return os_path(f"{self.buf_f}/{buf_filename(self.index, self.step)}")
    
    def next_filename(self):
        self.step += 1
        return os_path(f"{self.buf_f}/{buf_filename(self.index, self.step)}")

    def pipe_crop(self, v_length, v_res):
        pipeline = []
        if v_length >= 3:
            pipeline.append(trim_to_seconds(self.last_filename(), self.next_filename(), 2.8))
            print(f"Trimming video from {v_length} to {3} seconds")
        pipeline.append(resize_video(
            self.last_filename(), 
            self.next_filename(), 
            get_desired_resolution(v_res)
        ))
        return pipeline

    def pipe_crop_speedup(self, v_length, v_res):
        pipeline = []
        if v_length > 9:
            pipeline.append(trim_to_seconds(self.last_filename(), self.next_filename(), 9))
            print(f"Trimming video from {v_length} to {9} seconds")
            v_length = 9
        pipeline.append(resize_video(
            self.last_filename(), 
            self.next_filename(), 
            get_desired_resolution(v_res)
        ))
        if v_length > 3:
            pipeline.append(speedup(self.last_filename(), self.next_filename(), v_length / 2.8))
            print(f"Speeding up video from {v_length} to {3} seconds")
        return pipeline
    
    def pipe_speedup(self, v_length, v_res):
        pipeline = []
        if v_length > 59:
            pipeline.append(trim_to_seconds(self.last_filename(), self.next_filename(), 59))
            self.step += 1
            v_length = 59
        pipeline.append(resize_video(
            self.last_filename(), 
            self.next_filename(), 
            get_desired_resolution(v_res)
        ))
        if v_length > 3:
            pipeline.append(speedup(self.last_filename(), self.next_filename(), v_length / 2.8))
        return pipeline
