import tarfile

def extract_tarfile(path: str, target_directory: str):
    print(path)
    tar_file = tarfile.open(path, mode='r:gz')
    tar_file.extractall(path=target_directory)
