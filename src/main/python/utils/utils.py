# import os.path as path
from pathlib import Path

project_name = 'bittor'


def base_dir():
    p = __get_path(Path(__file__))
    return p


def __get_path(p):
    if p.name == project_name:
        return p
    else:
        return __get_path(p.parent)
