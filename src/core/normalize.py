import src.cli.commands as commands
from pathlib import Path
from dataclasses import dataclass


def normalize(cfg):
    # convert rellative paths to absolute paths
    cfg.zummarize_path = cfg.zummarize_path.resolve()
    cfg.log_path = cfg.log_path.resolve()

    if type(cfg) is commands.BasePlot:
        cfg.color = "red"  # dummy

    return cfg
