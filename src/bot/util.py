import os
from pathlib import Path

def get_desired_resolution(res):
        x, y = res[0], res[1]
        if x > y:
            x, y = 512, int(y / x * 512)
        else:
            x, y = int(x / y * 512), 512
        return [x, y]

def first_nonnone(iterable):
    for i in iterable:
        if i is not None:
            return i

def format_from_filename(filename: str) -> str:
    return filename.split(".")[-1]

def remove_file(path_str):
    path = Path(path_str)
    os.remove(path)

def os_path(path_str):
    path = Path(path_str)
    return str(path)

