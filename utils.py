from pathlib import Path


def is_dir(path: str):
    return Path(path).is_dir()
