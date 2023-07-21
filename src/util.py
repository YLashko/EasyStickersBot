import os
from pathlib import Path


def remove_file(path_str):
    path = Path(path_str)
    os.remove(path)

def os_path(path_str):
    path = Path(path_str)
    return str(path)

