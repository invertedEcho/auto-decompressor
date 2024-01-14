from pathlib import Path


def is_dir(path: str):
    path = Path(path)
    return path.is_dir() if path.is_absolute() else path.expanduser().is_dir()


def is_file(path: str):
    path = Path(path)
    return path.is_file() if path.is_absolute() else path.expanduser().is_file()
