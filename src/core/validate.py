from pathlib import Path
import os


def validate_log_paths(cfg):
    if cfg.log_paths is None:
        raise ValueError("Path to logfile directory not specified.")
    for log_path in cfg.log_paths:
        validate_log_path(log_path)


def validate_log_path(log_path):
    if not log_path.exists():
        raise FileNotFoundError(f"Path to logfile directory does not exist. Path: {log_path}")
    if not log_path.is_dir():
        raise NotADirectoryError(f"Path does not lead to a directory. Path: {log_path}")
    if not (any(log_path.glob("*.log")) or any(log_path.glob("*.err"))):
        raise ValueError(f"Directory does not contain a .log or .err file. Path: {log_path}")


def pre_validate_log_paths(cfg):
    if cfg.log_paths is None and cfg.r_log_paths is None:
        raise ValueError("Path to logfile directory not specified.")


def validate_zummarize_path(cfg):
    if cfg.zummarize_path is None:
        raise ValueError(f"Path to zummarize is not specified but required because no zummary exists in the log directoy. Path: {zummarize_path}")
    if not cfg.zummarize_path.exists():
        raise FileNotFoundError(f"zummarize binary does not exist. Path: {cfg.zummarize_path}")
    if not os.access(cfg.zummarize_path, os.X_OK):
        raise PermissionError(f"zummarize is not executable. Path: {cfg.zummarize_path}")
