from src.core.pipeline import run_pipeline
from src.cli.configbuilder import build_config
from src.core.configuration_data import PlotType
import typer
from typing import Annotated, Optional

app = typer.Typer()

base_raw: dict[str, Optional[str] | Optional[list[str]]] = {
    "zummarize_path": None,
    "log_paths": None,
    "r_log_paths": None,
    "config_path": None
}


@app.callback()
def base(zummarizepath: Annotated[Optional[str], typer.Option()] = None,
         logpaths: Annotated[Optional[list[str]], typer.Option()] = None,
         rlogpaths: Annotated[Optional[list[str]], typer.Option()] = None,
         configpath: Annotated[Optional[str], typer.Option()] = None):

    base_raw["zummarize_path"] = zummarizepath
    base_raw["log_paths"] = logpaths
    base_raw["r_log_paths"] = rlogpaths
    base_raw["config_path"] = configpath


@app.command()
def lineplot(color: Annotated[Optional[str], typer.Option()] = None):

    raw = {
        "base_raw": base_raw,
        "atr": {
            "color": color
        }
    }

    cfg = build_config(raw, PlotType.BasePlot)
    run_pipeline(cfg)
