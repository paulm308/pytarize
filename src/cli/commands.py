from src.core.pipeline import run_pipeline
from src.cli.configbuilder import build_config
from src.core.configuration_data import PlotType
import typer
from typing import Annotated, Optional

app = typer.Typer()


@app.command()
def base(zummarizepath: Annotated[Optional[str], typer.Option()] = None,
         logpaths: Annotated[Optional[list[str]], typer.Option()] = None,
         configpath: Annotated[Optional[str], typer.Option()] = None,
         color: Annotated[Optional[str], typer.Option()] = None):

    # set defaults:
    raw = {
        "zummarize_path": zummarizepath,
        "log_paths": logpaths,
        "config_path": configpath,
        "atr": {
            "color": color
        }
    }

    cfg = build_config(raw, PlotType.BasePlot)

    run_pipeline(cfg)
