from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class PlotType(Enum):
    LinePlot = 1,
    ScatterPlot = 2,
    CombinedPlot = 3
    # +---------------------+
    # | Add new plot option |
    # +---------------------+


@dataclass
class CFG:
    """
    Stores all options and arguments that can be specified as cli or in a config.
    """
    plot_type: PlotType                             # The type of the plot (LinePlot, ScatterPlot, CombinedPlot)
    zummarize_path: Path | None                     # The path to the zummarize executable
    log_paths: list[Path] | None                    # List of paths that lead to folders containing a zummary or .log and .err files
    r_log_paths: list[Path] | None                  # List of root directories that are recursively searched for log folders
    base_config_path: Path                          # The path to the base config (a config that is always called first)
    plot_config_paths: list[Path] | None            # List of paths that lead to config (.yaml) files
    zummarize_cli: list[str]                        # List of options that are only relevant for the zummarize script
    save_config: Path | None                        # The location where the output config should be saved
    global_atr: dict = field(default_factory=dict)  # Attributes that affect all plot types and handle data transformations
    atr: dict = field(default_factory=dict)         # All plot and styling specific options and arguments
