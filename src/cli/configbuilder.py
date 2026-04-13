import src.core.configuration_data as config_data
from src.cli.load_config import read_config
from src.cli.validate_config import validate_config_path
from src.cli.dictmerger import merge_dicts
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
                               log_paths=None,
                               r_log_paths=None,
                               base_config_path=base_config_path,
                               plot_config_path=plot_config_path,
                               atr=atr)
    return defaults


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
    if raw["log_paths"] is not None:
        cfg.log_paths = [Path(log_path) for log_path in raw["log_paths"]]
    if raw["r_log_paths"] is not None:
        cfg.r_log_paths = [Path(r_log_path) for r_log_path in raw["r_log_paths"]]
    cfg.atr = merge_dicts(cfg.atr, raw["atr"])

    return cfg
