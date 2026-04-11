from pathlib import Path
import os


def validate_log_path(cfg):
    log_path = cfg.log_path
    if not log_path.exists():
        raise FileNotFoundError("Path to logfile directory does not exist")
    if not log_path.is_dir():
        raise NotADirectoryError("Path does not lead to a directory")
    if not (any(log_path.glob("*.log")) or any(log_path.glob("*.err"))):
        raise ValueError("Directory does not contain a .log or .err file")


def check_if_zummary_exists(cfg):
    return (cfg.log_path / "zummary").exists()


def validate_zummarize_path(cfg):
    zummarize_path = cfg.zummarize_path
    if not zummarize_path.exists():
        raise FileNotFoundError("zummarize binary does not exist")

    if not os.access(zummarize_path, os.X_OK):
        raise PermissionError("zummarize is not executable")
