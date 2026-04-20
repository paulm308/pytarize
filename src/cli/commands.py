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

zummarize_specific_raw: dict[str, bool] = {
    "all": False,
    "sat": False,
    "unsat": False,
    "deep": False,
    "rank": False,
    "unsolved": False,
    "solved": False
}


@app.callback()
def base(zummarizepath: Annotated[Optional[str], typer.Option()] = None,
         logpaths: Annotated[Optional[list[str]], typer.Option()] = None,
         rlogpaths: Annotated[Optional[list[str]], typer.Option()] = None,
         configpath: Annotated[Optional[str], typer.Option()] = None,
         all: bool = typer.Option(False, "--all", "-a"),
         sat: bool = typer.Option(False, "--sat", "-s"),
         unsat: bool = typer.Option(False, "--unsat", "-u"),
         deep: bool = typer.Option(False, "--deep", "-d"),
         rank: bool = typer.Option(False, "--rank", "-r"),
         unsolved: bool = typer.Option(False, "--unsolved"),
         solved: bool = typer.Option(False, "--solved")):

    base_raw["zummarize_path"] = zummarizepath
    base_raw["log_paths"] = logpaths
    base_raw["r_log_paths"] = rlogpaths
    base_raw["config_path"] = configpath

    zummarize_specific_raw["all"] = all
    zummarize_specific_raw["sat"] = sat
    zummarize_specific_raw["unsat"] = unsat
    zummarize_specific_raw["deep"] = deep
    zummarize_specific_raw["rank"] = rank
    zummarize_specific_raw["unsolved"] = unsolved
    zummarize_specific_raw["solved"] = solved


@app.command()
def lineplot(color: Annotated[Optional[str], typer.Option()] = None):

    raw = {
        "base_raw": base_raw,
        "zummarize_specific_raw": zummarize_specific_raw,
        "atr": {
            "color": color
        }
    }

    cfg = build_config(raw, PlotType.BasePlot)
    run_pipeline(cfg)
