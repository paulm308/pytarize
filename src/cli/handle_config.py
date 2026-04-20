from src.cli.dictmerger import merge_dicts
import yaml
from pathlib import Path


def apply_config(config_path, cfg):
    with open(config_path, "r") as file:
        data = yaml.safe_load(file)
        if data is None:
            return cfg
        if "zummarize_path" in data.keys():
            cfg.zummarize_path = Path(data["zummarize_path"])
            del data["zummarize_path"]
        if "log_paths" in data.keys():
            cfg.log_paths = [Path(log_path) for log_path in data["log_paths"]]
            del data["log_paths"]
        if "r_log_paths" in data.keys():
            cfg.r_log_paths = [Path(r_log_path) for r_log_path in data["r_log_paths"]]
            del data["r_log_paths"]
        cfg.atr = merge_dicts(cfg.atr, data)
    return cfg
