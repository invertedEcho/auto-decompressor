from extractors import tar, zip

file_extension_to_extract_function = {
    "tar": tar.extract_tarfile,
    "zip": zip.extract_zip,
}

def extract_archive(path: str, file_extension: str, target_directory: str):
        maybe_extractor_function = file_extension_to_extract_function.get(
            file_extension
        )

        if maybe_extractor_function is None:
            return

        print(f"Extracting archive: {path}")
        maybe_extractor_function(path=path, target_directory=target_directory)
        print(f"Extracted archive in directory: {target_directory}")
