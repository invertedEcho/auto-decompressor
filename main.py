from pathlib import Path
from typing import Set

from watchfiles.main import FileChange

from extractors.zip import extract_zip
from extractors.tar import extract_tarfile

from watchfiles import Change, watch

from arguments import get_args

# TODO: Extract constants to some file
VERSION = "0.1.0"
SUPPORTED_ARCHIVES = ("tar", "zip")

# .crdownload is chromium, .part is firefox
PARTIAL_FILE_EXTENSIONS = (".crdownload", ".part")

mapping_file_extension_to_extract_function = {
    "tar": extract_tarfile,
    "zip": extract_zip,
}


def setup_logger():
    raise NotImplementedError("Not yet implemented.")


def main():
    arguments = get_args()
    watch_directory = arguments.watch_directory
    target_directory = arguments.target_directory

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


def get_file_extension(file: str):
    """
    Get's the file extension of the specified file

    TODO: Doesn't handle file extensions like `.tar.gz`
    """
    splitted = file.split(".")
    return splitted[1]


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
