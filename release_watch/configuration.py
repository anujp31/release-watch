import toml
from os.path import isfile, expanduser


class Config:
    def __init__(self):
        self.config_file_paths = ["~/.config/release-watch.toml"]
        self.conf = self.load_config()

    def load_config(self):
        for path in self.config_file_paths:
            p = expanduser(path)
            try:
                with open(p, "r") as f:
                    c = toml.load(f)
                return c
            except FileNotFoundError as e:
                raise e
