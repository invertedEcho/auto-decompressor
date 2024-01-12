import tarfile

def extract_tarfile(path: str):
    print(path)
    tar_file = tarfile.open(path, mode='r:gz')
    tar_file.extractall(path='/home/jakob/test2')
