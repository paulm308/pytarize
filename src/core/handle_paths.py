from pathlib import Path
import subprocess
from typing import List, Optional
import os


# bash path handling ------------------------------------------------------------------------------
def expand_with_bash(value: Optional[str]) -> List[str]:
    if value is None:
        return []

    result = subprocess.run(
        ["bash", "-c", f'printf "%s\\n" {value}'],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in result.stdout.splitlines() if line]


# recursive log path handling ---------------------------------------------------------------------
def is_log_dir(path: Path) -> bool:
    return (any(path.glob("*.log")) and any(path.glob("*.err")))


def find_log_dirs(base: Path) -> list[Path]:
    res = []
    if base.is_dir() and is_log_dir(base):
        res.append(base)

    for path in sorted(base.rglob("*")):
        if path.is_dir() and is_log_dir(path):
            res.append(path)

    return res


def extract_log_paths(cfg):
    if cfg.r_log_paths is None:
        return
    paths = []
    for r_log_path in cfg.r_log_paths:
        paths.extend(find_log_dirs(r_log_path))
    if cfg.log_paths is None:
        cfg.log_paths = paths
    else:
        cfg.log_paths.extend(paths)


# normalization -----------------------------------------------------------------------------------
def normalize(cfg):
    # convert rellative paths to absolute paths
    if cfg.zummarize_path is not None:
        cfg.zummarize_path = cfg.zummarize_path.expanduser().resolve()
    paths = []
    if cfg.log_paths is not None:
        for log_path in cfg.log_paths:
            paths.append(log_path.expanduser().resolve())

        # remove duplicates:
        seen = set()
        cfg.log_paths = []
        for path in paths:
            if path not in seen:
                seen.add(path)
                cfg.log_paths.append(path)

    cfg.base_config_path = cfg.base_config_path.expanduser().resolve()
    cfg.plot_config_path = cfg.base_config_path.expanduser().resolve()


def normalize_r_log_paths(cfg):
    # convert rellative paths to absolute paths
    if cfg.r_log_paths is not None:
        r_paths = []
        for r_log_path in cfg.r_log_paths:
            r_paths.append(r_log_path.expanduser().resolve())

        # remove duplicates:
        cfg.r_log_paths = list(set(r_paths))


# validation --------------------------------------------------------------------------------------
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
    if cfg.r_log_paths is not None:
        for path in cfg.r_log_paths:
            if not path.exists():
                raise FileNotFoundError(f"Path to directory does not exist. Path: {path}")


def validate_zummarize_path(cfg):
    if cfg.zummarize_path is None:
        raise ValueError(f"Path to zummarize is not specified but required because no zummary exists in the log directoy. Path: {cfg.zummarize_path}")
    if not cfg.zummarize_path.exists():
        raise FileNotFoundError(f"zummarize binary does not exist. Path: {cfg.zummarize_path}")
    if not os.access(cfg.zummarize_path, os.X_OK):
        raise PermissionError(f"zummarize is not executable. Path: {cfg.zummarize_path}")


def validate_config_path(config_path: Path):
    if not config_path.exists():
        raise FileNotFoundError(f"Path to config does not exist. Path: {config_path}")
    if not config_path.is_file():
        raise FileNotFoundError(f"Path does not lead to a file. Path: {config_path}")
    if not config_path.suffix == ".yaml":
        raise ValueError(f"Path does not lead to a .yaml file. Path: {config_path}")
