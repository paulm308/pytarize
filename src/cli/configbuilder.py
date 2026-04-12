import src.core.configuration_data as config_data
from src.cli.load_config import read_config
from src.cli.validate_config import validate_config_path
from pathlib import Path


def set_defaults(plot_type: config_data.PlotType):
    base_config_path = Path("config/base_config.yaml")
    plot_config_path = Path("")
    atr = {}

    match plot_type:
        case config_data.PlotType.BasePlot:
            plot_config_path = Path("config/plot_configs/baseplot.yaml")
            atr = {"color": "red"}  # dummy

    defaults = config_data.CFG(plot_type=plot_type,
                               zummarize_path=None,
                               log_path=None,
                               base_config_path=base_config_path,
                               plot_config_path=plot_config_path,
                               atr=atr)
    return defaults


def merge_dicts(base: dict, override: dict) -> dict:
    result = base.copy()

    for key, value in override.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = merge_dicts(result[key], value)
        elif value is not None:
            result[key] = value

    return result


def build_config(raw, plot_type: config_data.PlotType):
    # set defaults:
    cfg = set_defaults(plot_type)

    # base confic:
    cfg = read_config(cfg.base_config_path, cfg)

    # specific confics:
    if raw["config_path"] is not None:
        path = Path(raw["config_path"])
        validate_config_path(path)
        cfg = read_config(path, cfg)
    else:
        cfg = read_config(cfg.plot_config_path, cfg)

    # apply cli:
    if raw["zummarize_path"] is not None:
        cfg.zummarize_path = Path(raw["zummarize_path"])
    if raw["log_path"] is not None:
        cfg.log_path = Path(raw["log_path"])
    cfg.atr = merge_dicts(cfg.atr, raw["atr"])

    return cfg
