from src.bot.converter import Converter, ProcessPipeline, PipeModes
from src.bot.util import get_desired_resolution, first_nonnone, format_from_filename
from src.bot.image_converter import process_image_document
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
    res = [1280, 720]
    assert get_desired_resolution(res) == [512, 288]

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

def test_image():
    c = Converter("in", "buf", "out")
    with open("test_vids/test_image.png", "rb") as bytes_image:
        result = process_image_document(bytes_image.read()) # idk how to test images, just check if it not fails

def test_first_nonnone():
    assert first_nonnone([None, None, "Hello", None]) == "Hello"

def test_format_from_filename():
    assert format_from_filename("video.mp4") == "mp4"
    assert format_from_filename("photo.png...no.its.actually.jpg") == "jpg"
