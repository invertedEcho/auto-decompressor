import zipfile


def extract_zip(path: str, target_directory: str) -> None:
    file = zipfile.ZipFile(path)
    file.extractall(path=target_directory)
