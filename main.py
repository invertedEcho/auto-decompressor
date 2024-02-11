from pathlib import Path
import sys
import argparse
from typing import Set

from watchfiles.main import FileChange

from extractors.zip import extract_zip
from utils import is_dir
from extractors.tar import extract_tarfile

from watchfiles import Change, watch

# TODO: Extract constants to some file
VERSION = "0.1.0"
SUPPORTED_ARCHIVES = ("tar", "zip")

# .crdownload is chromium, .part is firefox
PARTIAL_FILE_EXTENSIONS = (".crdownload", ".part")

mapping_file_extension_to_extract_function = {
    "tar": extract_tarfile,
    "zip": extract_zip,
}


def setup_argparse():
    parser = argparse.ArgumentParser(
        prog="auto decompressor watching for new compressed files",
        description="Watches over a specified directory and automatically decompresses any found archive",
    )
    parser.add_argument("watch_directory", type=str)
    parser.add_argument("-t", "--target_directory", required=False)
    arguments = parser.parse_args()
    return arguments


def setup_logger():
    raise NotImplementedError("Not yet implemented.")


def check_arguments(watch_directory: str, target_directory: str | None):
    if target_directory is not None and not is_dir(target_directory):
        sys.exit(
            f"Invalid given target_directory: {target_directory}\nNot a directory."
        )

    if not is_dir(watch_directory):
        sys.exit(f"Invalid given watch_directory: {watch_directory}\nNot a directory.")


def main():
    arguments = setup_argparse()
    watch_directory = arguments.watch_directory
    target_directory = arguments.target_directory

    check_arguments(watch_directory, target_directory)

    print(
        f"""auto-uncompressor\nversion: {VERSION}\n
Running with options:
Watch directory: {watch_directory}
Target Directory: {target_directory if isinstance(target_directory, str) else "None, extracting in archives directory."}
""".strip()
    )

    for changes in watch(watch_directory):
        actual_target_directory = (
            target_directory if target_directory else watch_directory
        )
        handle_change(changes, actual_target_directory)


def get_file_extension(path: str):
    splitted = path.split(".")
    return splitted[1]


def is_relevant_file(path: str, event: Change):
    if not event == Change.added:
        return False

    # Check if the file is a partial file
    if path.endswith(PARTIAL_FILE_EXTENSIONS):
        return False
    # Check if the file is a supported archive
    if not path.endswith(SUPPORTED_ARCHIVES):
        return False

    # Check if file is of size 0
    path2 = Path(path)
    stat = path2.stat()
    if stat.st_size == 0:
        return False

    return True


def handle_change(changes: Set[FileChange], target_directory: str):
    for change in changes:
        event_type, path = change
        is_relevant_file2 = is_relevant_file(path=path, event=event_type)
        if not is_relevant_file2:
            continue
        print(f"Relevant file: {path}")
        file_extension = get_file_extension(path)
        print(f"Detected file extension: {file_extension}")
        maybe_extractor_function = mapping_file_extension_to_extract_function.get(
            file_extension
        )

        if maybe_extractor_function is None:
            continue

        print(f"Extracting archive: {path}")
        maybe_extractor_function(path=path, target_directory=target_directory)
        print(f"Extracted archive in directory: {target_directory}")


if __name__ == "__main__":
    main()
