from pathlib import Path


def is_dir(source_path: str):
    target_path = Path(source_path)
    return (
        target_path.is_dir()
        if target_path.is_absolute()
        else target_path.expanduser().is_dir()
    )


def is_file(source_path: str):
    target_path = Path(source_path)
    return (
        target_path.is_file()
        if target_path.is_absolute()
        else target_path.expanduser().is_file()
    )
