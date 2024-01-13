from pathlib import Path


def is_dir(path: str):
    return Path(path).is_dir()

def is_empty_file(path: str) -> bool:
    return Path(path).stat().st_size == 0
