import subprocess
import time
from config import OS_TYPE

def run_command(command: list[str], record_time = False) -> None:
    try:
        if record_time:
            a = time.time()

        command_str = " ".join(command)
        if OS_TYPE == "linux":
            command_str = command_str.replace("\\", "/")
        p = subprocess.run(command_str, check=True, capture_output=True, text=True, shell=True)

        if record_time:
            print(f"Done! In {round(time.time() - a, 4)} seconds")
        return p.stdout
    except subprocess.CalledProcessError as e:
        raise Exception("Exception during command execution: {}".format(e))

def mp4_to_webm(input, output):
    return [
        "ffmpeg",
        "-i", input,
        "-c:v",
        "libvpx-vp9",
        "-deadline", "realtime",
        "-cpu-used", "6",
        "-b:v 384k",
        "-c:a",
        "libopus",
        "-an",
        output
    ]

def trim_to_seconds(input, output, s=9):
    s = max(min(s, 59), 1)                          # cut seconds to 1 <= s <= 59
    s_str = "" if s >= 10 else "0" + str(float(s))    # append 0 if necessary
    return [
        "ffmpeg",
        "-ss", f"00:00:00",
        "-i", input,
        "-c", "copy",
        "-t", f"00:00:{s_str}",
        output
    ]

def speedup(input, output, speedup_rate: 3):
    return [
        "ffmpeg",
        "-i", input, 
        "-vf", f"setpts={1 / speedup_rate}*PTS", output
    ]

def video_length(input):
    return [
        "ffprobe", 
        "-v", "error", 
        "-show_entries", "format=duration", 
        "-of", "default=noprint_wrappers=1:nokey=1", input]

def video_resolution(input):
    return [
        "ffprobe", 
        "-v", "error", 
        "-select_streams", "v:0", 
        "-show_entries", "stream=width,height", 
        "-of", "csv=s=x:p=0",
        input
    ]

def resize_video(input, output, scale: list[int]):
    return [
        "ffmpeg",
        "-i", input,
        "-vf", f"scale={scale[0]}:{scale[1]}",
        output
    ]
