import sys
import time
import argparse
from tarfile import ReadError
from typing import Tuple

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

from extractors.zip import extract_zip
from utils import is_dir
from extractors.tar import extract_tarfile

VERSION = "waytooearlyman"

SUPPORTED_ARCHIVES = ["tar.gz", "zip"]

mapping_file_extension_to_extract_function = {
    "tar.gz": extract_tarfile,
    "zip": extract_zip,
}


def setup_argparse():
    parser = argparse.ArgumentParser(
        prog="auto uncompressor watching for new compressed files",
        description="Watches over a specified directory and automatically uncompresses any found archive",
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

    watcher = WatchDog(watch_directory, target_directory)
    watcher.run()


class WatchDog:
    def __init__(self, watch_directory, target_directory) -> None:
        self.watch_directory = watch_directory
        self.target_directory = (
            target_directory if target_directory is not None else watch_directory
        )
        self.observer = Observer()

    def run(self):
        watch_dog_handler = WatchDogEventHandler(target_directory=self.target_directory)
        self.observer.schedule(watch_dog_handler, self.watch_directory, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Watchdog stopped")

        self.observer.join()


def get_file_extension_and_is_supported(path: str) -> Tuple[str, bool]:
    """TODO: Don't just check string-wise but use something to detect the filetype -> `file`?"""
    if not path.__contains__("."):
        return "", False
    file_name_splitted = path.split(".")

    file_extension = file_name_splitted[-1]

    if len(file_name_splitted) > 2:
        second_extension = file_name_splitted[-1]
        first_extension = file_name_splitted[-2]
        file_extension = f"{first_extension}.{second_extension}"

    return file_extension, file_extension in SUPPORTED_ARCHIVES


def process_event(event_type: str, path: str, target_directory: str):
    if event_type not in ("created", "modified"):
        return

    if path.endswith("part"):
        return

    file_extension, result = get_file_extension_and_is_supported(path)
    if not result:
        return

    print(f"Extracting archive: {path}...")
    try:
        mapping_file_extension_to_extract_function.get(file_extension)(
            path=path, target_directory=target_directory
        )
    except ReadError as e:
        if event_type == "created" and e.args[0] == "empty file":
            return

    print(f"Finished extracting {path}.\n")


class WatchDogEventHandler(FileSystemEventHandler):
    """on_created event: Relevant for cutting and pasting an archive
    on_modified event: Downloading an archive into watch directory -> we assume that this because of getting renamed after .part files
    """

    def __init__(self, target_directory: str):
        self.target_directory = target_directory

    def on_any_event(self, event: FileSystemEvent):
        process_event(
            event.event_type, event.src_path, target_directory=self.target_directory
        )


if __name__ == "__main__":
    main()
