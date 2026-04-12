import yaml
from pathlib import Path


def read_config(config_path, cfg):
    with open(config_path, "r") as file:
        data = yaml.safe_load(file)
        if data is None:
            return cfg
        if "zummarize_path" in data.keys():
            cfg.zummarize_path = Path(data["zummarize_path"])
            del data["zummarize_path"]
        if "log_path" in data.keys():
            cfg.log_path = Path(data["log_path"])
            del data["log_path"]

        cfg.atr = cfg.atr | data
    return cfg
