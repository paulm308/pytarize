from src.core.configuration_data import CFG, PlotType
from src.cli.handle_config import apply_config, construct_combined_cfg, pre_construct_configpaths, count_plot_configs
from src.cli.dictmerger import merge_dicts
from src.cli.handle_zummarize_options import create_zummarize_options
from pathlib import Path


def set_defaults(plot_type: PlotType):
    """
    This function creates and initializes the configuration (cfg) object with default values.

    Parameters:
    plot_type (PlotType): The type of the plot (LinePlot, ScatterPlot or CombinedPlot).

    Returns:
    CFG: The initialized configuration object.
    """
    base_config_path = Path("config/base_config.yaml")  # change default path to base config
    plot_config_paths = None
    atr = {}
    def_global_atr = {}
    match plot_type:
        case PlotType.LinePlot:
            atr = {
                "colors": list(reversed(['#9400d3',
                                         '#009e73',
                                         '#56b4e9',
                                         '#e69f00',
                                         '#f0e442',
                                         '#0072b2',
                                         '#e51e10',
                                         '#000000'])),
                "markers": ["o", "+", "x", "s", "^", "v", "d"],
                "output": "plot.png",
                "font_family": "serif"
            }
        case PlotType.ScatterPlot:
            atr = {
                "colors": ['#9400d3',
                           '#000000',
                           '#e51e10'],
                "markers": ["x", "o", "+"],
                "output": "plot.png",
                "font_family": "serif"
            }
        case PlotType.CombinedPlot:
            atr = {
                "colors": list(reversed(['#9400d3',
                                         '#009e73',
                                         '#56b4e9',
                                         '#e69f00',
                                         '#f0e442',
                                         '#0072b2',
                                         '#e51e10',
                                         '#000000'])),
                "markers": ["o", "+", "x", "s", "^", "v", "d"],
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
    """
    Creates the final configuration object by combining the default values with the configs and the cli.

    Parameters:
    raw (dict): The unprocessed cli arguments and options.
    plot_type (PlotType): The type of the plot (LinePlot, ScatterPlot or CombinedPlot).

    Returns:
    CFG: The final configuration object.
    """
    # set defaults:
    cfg = set_defaults(plot_type)

    # base confic:
    if cfg.base_config_path.exists():
        cfg = apply_config(cfg.base_config_path, cfg)

    # specific confics:
    if raw["base_raw"]["config_paths"] is not None:
        pre_construct_configpaths(raw["base_raw"]["config_paths"], cfg)
        if count_plot_configs(raw["base_raw"]["config_paths"]) == 0 and cfg.plot_config_paths is not None:
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
