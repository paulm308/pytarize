from pathlib import Path


def is_log_dir(path: Path) -> bool:
    return (any(path.glob("*.log")) and any(path.glob("*.err")))


def find_log_dirs(base: Path) -> list[Path]:
    res = []
    if base.is_dir() and is_log_dir(base):
        res.append(base)

    for path in base.rglob("*"):
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
