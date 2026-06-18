from src.core.configuration_data import CFG, PlotType
from src.cli.handle_config import apply_config
from src.cli.validate_config import validate_config_path
from src.cli.dictmerger import merge_dicts
from src.cli.handle_zummarize_options import create_zummarize_options
from pathlib import Path


def set_defaults(plot_type: PlotType):
    base_config_path = Path("config/base_config.yaml")  # change default path to base config
    plot_config_paths = None
    atr = {}

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
                   atr=atr)

    return defaults


def construct_combined_cfg(paths: list[Path], cfg):
    path = Path(paths[0])
    validate_config_path(path)
    cfg = apply_config(path, cfg)
    for i in range(1, len(paths)):
        path = Path(paths[i])
        validate_config_path(path)
        cfg = apply_config(path, cfg)


def build_config(raw, plot_type: PlotType):
    # set defaults:
    cfg = set_defaults(plot_type)

    # base confic:
    if cfg.base_config_path.exists():
        cfg = apply_config(cfg.base_config_path, cfg)

    # specific confics:
    if raw["base_raw"]["config_paths"] is not None:
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
    cfg.atr = merge_dicts(cfg.atr, raw["atr"], False)
    cfg.zummarize_cli = create_zummarize_options(raw["zummarize_specific_raw"])

    return cfg
