from pathlib import Path
import os


def validate_log_path(cfg):
    log_path = cfg.log_path
    if log_path is None:
        raise ValueError("Path to logfile directory not specified.")
    if not log_path.exists():
        raise FileNotFoundError(f"Path to logfile directory does not exist. Path: {log_path}")
    if not log_path.is_dir():
        raise NotADirectoryError(f"Path does not lead to a directory. Path: {log_path}")
    if not (any(log_path.glob("*.log")) or any(log_path.glob("*.err"))):
        raise ValueError(f"Directory does not contain a .log or .err file. Path: {log_path}")


def check_if_zummary_exists(cfg):
    return (cfg.log_path / "zummary").exists()


def validate_zummarize_path(cfg):
    zummarize_path = cfg.zummarize_path
    if zummarize_path is None:
        raise ValueError(f"Path to zummarize is not specified but required because no zummary exists in the log directoy. Path: {zummarize_path}")
    if not zummarize_path.exists():
        raise FileNotFoundError(f"zummarize binary does not exist. Path: {zummarize_path}")
    if not os.access(zummarize_path, os.X_OK):
        raise PermissionError(f"zummarize is not executable. Path: {zummarize_path}")
