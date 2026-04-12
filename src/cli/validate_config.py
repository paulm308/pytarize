from pathlib import Path


def validate_config_path(config_path: Path):
    if not config_path.exists():
        raise FileNotFoundError(f"Path to logfile directory does not exist. Path: {config_path}")
    if not config_path.is_file():
        raise FileNotFoundError(f"Path does not lead to a file. Path: {config_path}")
    if not config_path.suffix == "yaml":
        raise ValueError(f"Path does not lead to a .yaml file. Path: {config_path}")
