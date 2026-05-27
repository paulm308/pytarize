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
    plot_type: PlotType
    zummarize_path: Path | None
    log_paths: list[Path] | None
    r_log_paths: list[Path] | None
    base_config_path: Path
    plot_config_path: Path | None
    zummarize_cli: list[str]
    save_config: Path | None
    atr: dict = field(default_factory=dict)
