from src.converter import Converter, ProcessPipeline, PipeModes
import pytest
import os
import shutil

def test_clear_folder():
    c = Converter("in", "buf", "out")
    with open("out/foo.txt", "w") as f:
        f.write("Testfile")
    c.clear_folder(c.out_f)
    assert len(os.listdir("out")) == 0

def test_desired_resolution():
    p = ProcessPipeline("foo", 0)
    res = [1280, 720]
    assert p.get_desired_resolution(res) == [512, 288]

def test_crop_pipe():
    c = Converter("in", "buf", "out")
    shutil.copy(f"{os.getcwd()}\\test_vids\\animation.gif.mp4", f"{os.getcwd()}\\in\\animation.gif.mp4")
    c.create_and_run_pipe("animation.gif.mp4", PipeModes.Crop)
    assert len(os.listdir(f"{os.getcwd()}\\out")) == 1
    c.clear_folder(c.out_f)

def test_cropspeedup_pipe():
    c = Converter("in", "buf", "out")
    shutil.copy(f"{os.getcwd()}\\test_vids\\animation.gif.mp4", f"{os.getcwd()}\\in\\animation.gif.mp4")
    c.create_and_run_pipe("animation.gif.mp4", PipeModes.CropAndSpeedup)
    assert len(os.listdir(f"{os.getcwd()}\\out")) == 1
    c.clear_folder(c.out_f)

def test_speedup_pipe():
    c = Converter("in", "buf", "out")
    shutil.copy(f"{os.getcwd()}\\test_vids\\animation.gif.mp4", f"{os.getcwd()}\\in\\animation.gif.mp4")
    c.create_and_run_pipe("animation.gif.mp4", PipeModes.Speedup)
    assert len(os.listdir(f"{os.getcwd()}\\out")) == 1
    c.clear_folder(c.out_f)
