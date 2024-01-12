import tarfile

def extract_tarfile(path: str):
    print(path)
    with tarfile.open(path) as tar_file:
        print("klsjdfkljsdfk")
        # List all members in the archive
        for member in tar_file.getmembers():
            print(member.name)
    tar_file = tarfile.open(path, mode='r:gz')
    tar_file.extractall(path='/home/jakob/test2')
