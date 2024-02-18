import toml
from utils import is_dir, is_file
from pathlib import Path

from typing import Any

CONFIG_DIR = "~/.config/auto-decompressor"
CONFIG_PATH = f"{CONFIG_DIR}/config.toml"

# TODO: Don't use any
def validate_config(config: dict[str, Any]):
    match config:
        case {"overwrite-existing-dirs": bool()}:
            pass
        case _:
            raise ValueError("Config validation failed.")


def create_config_if_not_exists():
    if not is_dir(CONFIG_DIR):
        path_obj = Path(CONFIG_DIR)
        expanded_config_dir_path = path_obj.expanduser()
        expanded_config_dir_path.mkdir()

    if not is_file(CONFIG_PATH):
        path_obj = Path(CONFIG_PATH)
        expanded_config_file_path = path_obj.expanduser()
        expanded_config_file_path.touch()

        with open(expanded_config_file_path, "w") as config_file:
            config_file.write("overwrite-existing-dirs = false")



def load_config() -> dict[str, Any]:
    create_config_if_not_exists()
    path_obj = Path(CONFIG_PATH)
    expanded_config_file_path = path_obj.expanduser()

    with open(expanded_config_file_path, "r") as f:
        config = toml.loads(f.read())
        validate_config(config)
        return config
