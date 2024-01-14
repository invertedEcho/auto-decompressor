import tarfile


def extract_tarfile(path: str, target_directory: str):
    tar_file = tarfile.open(path)
    tar_file.extractall(path=target_directory)
