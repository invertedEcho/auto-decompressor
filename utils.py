from pathlib import Path


def is_dir(path: str):
    path2 = Path(path)
    return path2.is_dir() if path2.is_absolute() else path2.expanduser().is_dir()


def is_file(path: str):
    path2 = Path(path)
    return path2.is_file() if path2.is_absolute() else path2.expanduser().is_file()
