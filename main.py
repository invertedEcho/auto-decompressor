from pathlib import Path
from typing import Set

from watchfiles.main import FileChange

from watchfiles import Change, watch

from arguments import get_args
from config import load_config
from extractors import extract_archive
from utils import get_file_extension

VERSION = "0.1.0"
SUPPORTED_ARCHIVES = (".tar", ".zip", ".gz")

# .crdownload is chromium, .part is firefox
PARTIAL_FILE_EXTENSIONS = (".crdownload", ".part")


def setup_logger():
    raise NotImplementedError("Not yet implemented.")


def main():
    arguments = get_args()
    watch_directory = arguments.watch_directory
    target_directory = arguments.target_directory

    config = load_config()

    print(
        f"""auto-uncompressor\nversion: {VERSION}\n
Running with options:
Watch directory: {watch_directory}
Target Directory: {target_directory if isinstance(target_directory, str) else "None, extracting in archives directory."}

Config:
{config}
""".strip()
    )

    for changes in watch(watch_directory):
        actual_target_directory = (
            target_directory if target_directory else watch_directory
        )
        handle_change(changes, actual_target_directory)


def is_file_relevant(path: str, event: Change):
    if not event == Change.added:
        return False

    if path.endswith(PARTIAL_FILE_EXTENSIONS):
        return False

    if not path.endswith(SUPPORTED_ARCHIVES):
        return False

    target_path = Path(path)
    stat = target_path.stat()
    if stat.st_size == 0:
        return False

    return True


def handle_change(changes: Set[FileChange], target_directory: str):
    for change in changes:
        event_type, path = change
        is_relevant_file = is_file_relevant(path=path, event=event_type)
        if not is_relevant_file:
            continue
        print(f"Relevant file: {path}")
        file_extension = get_file_extension(path)
        print(f"Detected file extension: {file_extension}")

        extract_archive(
            path=path, file_extension=file_extension, target_directory=target_directory
        )


if __name__ == "__main__":
    main()
