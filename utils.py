import os
from pathlib import Path


def is_dir(source_path: str):
    """
    Check's whether the specified file path is a directory.

    This function both supports absolute and relative file paths.
    """
    target_path = Path(source_path)
    return (
        target_path.is_dir()
        if target_path.is_absolute()
        else target_path.expanduser().is_dir()
    )


def is_file(source_path: str):
    """
    Check's whether the specified file path is a file.

    This function both supports absolute and relative file paths.
    """
    target_path = Path(source_path)
    return (
        target_path.is_file()
        if target_path.is_absolute()
        else target_path.expanduser().is_file()
    )


def get_file_extension(file: str):
    """
    Get's the file extension of the specified file.
    """
    splitted = file.split(".")
    return splitted[-1]
