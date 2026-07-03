from src.cli.dictmerger import merge_dicts
import yaml
from pathlib import Path
from src.core.configuration_data import PlotType
from src.core.handle_paths import validate_config_path


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
        set_default_plot_config_paths(cfg, data)
        cfg.atr = merge_dicts(cfg.atr, data, False)
    return cfg


def set_default_plot_config_paths(cfg, data):
    if "config_paths" in data.keys() and data["config_paths"] is not None:
        if (
            cfg.plot_type == PlotType.LinePlot
            and "lineplot" in data["config_paths"].keys()
            and data["config_paths"]["lineplot"] is not None
        ):
            cfg.plot_config_paths = data["config_paths"]["lineplot"]
        elif (
            cfg.plot_type == PlotType.ScatterPlot and
            "scatterplot" in data["config_paths"].keys()
            and data["config_paths"]["scatterplot"] is not None
        ):
            cfg.plot_config_paths = data["config_paths"]["scatterplot"]
        elif (
            cfg.plot_type == PlotType.CombinedPlot and
            "combinedplot" in data["config_paths"].keys()
            and data["config_paths"]["combinedplot"] is not None
        ):
            cfg.plot_config_paths = data["config_paths"]["combinedplot"]
        # +-------------------+
        # | Add new plottypes |
        # +-------------------+

        del data["config_paths"]


def construct_combined_cfg(paths: list[Path], cfg):
    path = Path(paths[0])
    validate_config_path(path)
    cfg = apply_config(path, cfg)
    for i in range(1, len(paths)):
        path = Path(paths[i])
        validate_config_path(path)
        cfg = apply_config(path, cfg)


def pre_construct_configpaths(paths: list[Path], cfg):
    for path in paths:
        path = Path(path)
        validate_config_path(path)
        with open(path, "r") as file:
            data = yaml.safe_load(file)
            set_default_plot_config_paths(cfg, data)


def count_plot_configs(paths: list[Path], cfg) -> int:
    ctr = 0
    for path in paths:
        path = Path(path)
        validate_config_path(path)
        with open(path, "r") as file:
            data = yaml.safe_load(file)
            if "zummarize_path" in data.keys():
                del data["zummarize_path"]
            if "log_paths" in data.keys():
                del data["log_paths"]
            if "r_log_paths" in data.keys():
                del data["r_log_paths"]
            if "config_paths" in data.keys():
                del data["config_paths"]
            if data:
                ctr += 1
    return ctr
