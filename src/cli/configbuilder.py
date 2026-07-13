from src.core.configuration_data import CFG, PlotType
from src.cli.handle_config import apply_config, construct_combined_cfg, pre_construct_configpaths, count_plot_configs
from src.cli.dictmerger import merge_dicts
from src.cli.handle_zummarize_options import create_zummarize_options
from pathlib import Path


def set_defaults(plot_type: PlotType):
    base_config_path = Path("config/base_config.yaml")  # change default path to base config
    plot_config_paths = None
    atr = {}
    def_global_atr = {}
    match plot_type:
        case PlotType.LinePlot:
            atr = {
                "colors": ["red"],
                "markers": ["x"],
                "output": "plot.png",
                "font_family": "serif"
            }
        case PlotType.ScatterPlot:
            atr = {
                "colors": ["red"],
                "markers": ["x"],
                "output": "plot.png",
                "font_family": "serif"
            }
        case PlotType.CombinedPlot:
            atr = {
                "colors": ["red"],
                "markers": ["x"],
                "output": "plot.png",
                "font_family": "serif"
            }
        # +------------------------------------+
        # | Add default values for new options |
        # +------------------------------------+
    defaults = CFG(plot_type=plot_type,
                   zummarize_path=None,
                   log_paths=None,
                   r_log_paths=None,
                   base_config_path=base_config_path,
                   plot_config_paths=plot_config_paths,
                   zummarize_cli=[],
                   save_config=None,
                   global_atr=def_global_atr,
                   atr=atr)

    return defaults


def build_config(raw, plot_type: PlotType):
    # set defaults:
    cfg = set_defaults(plot_type)

    # base confic:
    if cfg.base_config_path.exists():
        cfg = apply_config(cfg.base_config_path, cfg)

    # specific confics:
    if raw["base_raw"]["config_paths"] is not None:
        pre_construct_configpaths(raw["base_raw"]["config_paths"], cfg)
        if count_plot_configs(raw["base_raw"]["config_paths"], cfg) == 0 and cfg.plot_config_paths is not None:
            construct_combined_cfg(cfg.plot_config_paths, cfg)
        else:
            construct_combined_cfg(raw["base_raw"]["config_paths"], cfg)
    elif cfg.plot_config_paths is not None:
        construct_combined_cfg(cfg.plot_config_paths, cfg)

    # apply cli:
    if raw["base_raw"]["zummarize_path"] is not None:
        cfg.zummarize_path = Path(raw["base_raw"]["zummarize_path"])
    if raw["base_raw"]["log_paths"] is not None:
        cfg.log_paths = [Path(log_path) for log_path in raw["base_raw"]["log_paths"]]
    if raw["base_raw"]["r_log_paths"] is not None:
        cfg.r_log_paths = [Path(r_log_path) for r_log_path in raw["base_raw"]["r_log_paths"]]
    if raw["base_raw"]["save_config"] is not None:
        cfg.save_config = Path(raw["base_raw"]["save_config"])

    cfg.global_atr = raw["global_atr"]
    cfg.atr = merge_dicts(cfg.atr, raw["atr"], False)
    cfg.zummarize_cli = create_zummarize_options(raw["zummarize_specific_raw"])

    return cfg
