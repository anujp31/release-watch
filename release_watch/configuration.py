import toml
from os.path import isfile, expanduser


class Config:
    def __init__(self):
        self.config_file_paths = ["~/.config/release-watch/config.toml"]
        self.conf = self.load_config()

    def load_config(self):
        for path in self.config_file_paths:
            p = expanduser(path)
            if isfile(p):
                with open(p, "r") as f:
                    c = toml.load(f)
                return c
        else:
            raise Exception("No config file found")
