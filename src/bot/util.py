import os
from pathlib import Path

def get_desired_resolution(res):
        max_res = max(res)
        rate = 512 / max_res
        x = int(res[0] * rate)
        y = int(res[1] * rate)
        x -= x % 2
        y -= y % 2
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

