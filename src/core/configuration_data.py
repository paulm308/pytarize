from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class PlotType(Enum):
    BasePlot = 1


@dataclass
class CFG:
    plot_type: PlotType
    zummarize_path: Path | None
    log_paths: list[Path] | None
    r_log_paths: list[Path] | None
    base_config_path: Path
    plot_config_path: Path
    zummarize_cli: list[str]
    atr: dict = field(default_factory=dict)
