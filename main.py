import sys
import time
import argparse
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from tar import extract_tarfile

SUPPORTED_ARCHIVES = ['tar.gz']

def setup_argparse():
    parser = argparse.ArgumentParser(
        prog="auto uncompressor watching for new compressed files",
        description="Watches over a specified directory and automatically uncompresses any found archive",
    )
    parser.add_argument("target_directory")
    arguments = parser.parse_args()
    return arguments

def is_dir(path: str):
    return Path(path).is_dir()

def setup_logger():
    raise Exception("not yet implemented")

def main():
    arguments = setup_argparse()
    target_directory = arguments.target_directory

    if not is_dir(target_directory):
        sys.exit(f'Invalid target directory: {target_directory}\nNot a directory.')

    watcher = WatchDog(target_directory)
    watcher.run()

class WatchDog:
    def __init__(self, target_directory):
        self.target_directory = target_directory
        self.observer = Observer()

    def run(self):
        watch_dog_handler = WatchDogHandler()
        self.observer.schedule(watch_dog_handler, self.target_directory, recursive=True)
        self.observer.start()
        
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Watchdog stopped")

        self.observer.join()

def is_archive_supported(path: str):
    """TODO: Don't just check string-wise but use something to detect the filetype -> `file`?"""
    if not path.__contains__('.'):
        print("file doesnt contain a dot")
        # TODO Fix this
        return 'fileDoesntContainDot', False 
    file_name_splitted = path.split(".")

    file_extension = file_name_splitted[-1]

    if len(file_name_splitted) > 2:
        print("this file has more than two dots, combining it  together")
        print(f" splitted: {file_name_splitted}")
        second_extension = file_name_splitted[-1]
        first_extension = file_name_splitted[-2]
        file_extension = f'{first_extension}.{second_extension}'
        
    print(f"found file_extension: {file_extension}")
    return file_extension, file_extension in SUPPORTED_ARCHIVES

class WatchDogHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(event)

    def on_created(self, event):
            src_path = event.src_path
            print(f"we got a new file! {src_path}")
            result = is_archive_supported(src_path)
            if not result[1]:
                print(f"Unsupported archive: {result[0]}")
            match result[0]:
                case 'tar.gz':
                    print('exxtracting archive')
                    extract_tarfile(src_path)

            
 
if __name__ == "__main__":
    main()
