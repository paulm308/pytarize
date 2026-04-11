import src.core.pipeline as pipeline
import typer
from dataclasses import dataclass
from pathlib import Path

app = typer.Typer()


@dataclass
class CFG:
    zummarize_path: Path
    log_path: Path


@dataclass
class BasePlot(CFG):
    color: str


@app.command()
def base(zummarize_path: str,
         log_path: str):
    cfg = BasePlot(zummarize_path=Path(zummarize_path),
                   log_path=Path(log_path),
                   color="red")  # dummy
    pipeline.run_pipeline(cfg)
