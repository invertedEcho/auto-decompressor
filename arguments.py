import sys
import argparse

from utils import is_dir


def get_args():
    parser = argparse.ArgumentParser(
        prog="auto decompressor watching for new compressed files",
        description="Watches over a specified directory and automatically decompresses any found archive",
    )
    parser.add_argument("watch_directory", type=str)
    parser.add_argument("-t", "--target_directory", required=False)
    arguments = parser.parse_args()

    check_arguments(
        watch_directory=arguments.watch_directory,
        target_directory=arguments.target_directory,
    )

    return arguments


def check_arguments(watch_directory: str, target_directory: str | None):
    if target_directory is not None and not is_dir(target_directory):
        sys.exit(
            f"Invalid given target_directory: {target_directory}\nNot a directory."
        )

    if not is_dir(watch_directory):
        sys.exit(f"Invalid given watch_directory: {watch_directory}\nNot a directory.")
