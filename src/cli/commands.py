from src.core.pipeline import run_pipeline
from src.cli.configbuilder import build_config
from src.core.configuration_data import PlotType
import typer
from typing import Annotated, Optional
import shlex

app = typer.Typer()

base_raw: dict[str, Optional[str] | Optional[list[str]]] = {
    "zummarize_path": None,
    "log_paths": None,
    "r_log_paths": None,
    "config_path": None
}

zummarize_specific_raw: dict[str, bool | Optional[int]] = {
    "verbose": None,
    "force": False,
    "ignore": False,
    "just": False,
    "no-warnings": False,
    "all": False,
    "sat": False,
    "unsat": False,
    "deep": False,
    "rank": False,
    "unsolved": False,
    "solved": False,
    "filter": False,
    "cmp": False,
    "no-write": False,
    "no-bounds": False,
    "force-real": False,
    "force-time": False
}


@app.callback()
def base(zummarizepath: Annotated[Optional[str], typer.Option()] = None,
         logpaths: Annotated[Optional[str], typer.Option()] = None,
         rlogpaths: Annotated[Optional[str], typer.Option()] = None,
         configpath: Annotated[Optional[str], typer.Option()] = None,
         verbose: Annotated[Optional[int], typer.Option("-v")] = None,
         force: bool = typer.Option(False, "--force", "-f"),
         ignore: bool = typer.Option(False, "--ignore", "-i"),
         just: bool = typer.Option(False, "--just", "-j"),
         no_warnings: bool = typer.Option(False, "--no-warnings", "-n"),
         all: bool = typer.Option(False, "--all", "-a"),
         sat: bool = typer.Option(False, "--sat", "-s"),
         unsat: bool = typer.Option(False, "--unsat", "-u"),
         deep: bool = typer.Option(False, "--deep", "-d"),
         rank: bool = typer.Option(False, "--rank", "-r"),
         unsolved: bool = typer.Option(False, "--unsolved"),
         solved: bool = typer.Option(False, "--solved"),
         filter: bool = typer.Option(False, "--filter"),
         cmp: bool = typer.Option(False, "--cmp"),
         no_write: bool = typer.Option(False, "--no-write"),
         no_bounds: bool = typer.Option(False, "--no-bounds"),
         force_real: bool = typer.Option(False, "--force-real"),
         force_time: bool = typer.Option(False, "--force-time")):

    base_raw["zummarize_path"] = zummarizepath
    base_raw["log_paths"] = None if logpaths is None else shlex.split(logpaths)
    base_raw["r_log_paths"] = None if rlogpaths is None else shlex.split(rlogpaths)
    base_raw["config_path"] = configpath

    zummarize_specific_raw["verbose"] = verbose
    zummarize_specific_raw["force"] = force
    zummarize_specific_raw["ignore"] = ignore
    zummarize_specific_raw["just"] = just
    zummarize_specific_raw["no-warnings"] = no_warnings
    zummarize_specific_raw["all"] = all
    zummarize_specific_raw["sat"] = sat
    zummarize_specific_raw["unsat"] = unsat
    zummarize_specific_raw["deep"] = deep
    zummarize_specific_raw["rank"] = rank
    zummarize_specific_raw["unsolved"] = unsolved
    zummarize_specific_raw["solved"] = solved
    zummarize_specific_raw["filter"] = filter
    zummarize_specific_raw["cmp"] = cmp
    zummarize_specific_raw["no-write"] = no_write
    zummarize_specific_raw["no-bounds"] = no_bounds
    zummarize_specific_raw["force-real"] = force_real
    zummarize_specific_raw["force-time"] = force_time


@app.command()
def lineplot(colors: Annotated[Optional[str], typer.Option()] = None,
             markers: Annotated[Optional[str], typer.Option()] = None,
             cactus: bool = typer.Option(False, "--cactus"),
             show_solved: bool = typer.Option(False, "--show-solved"),
             center: bool = typer.Option(False, "--center"),
             ymin: Annotated[Optional[float], typer.Option()] = None,
             xmin: Annotated[Optional[float], typer.Option()] = None,
             ymax: Annotated[Optional[float], typer.Option()] = None,
             xmax: Annotated[Optional[float], typer.Option()] = None,
             xlegend: Annotated[Optional[float], typer.Option()] = None,
             ylegend: Annotated[Optional[float], typer.Option()] = None,
             limit: Annotated[Optional[float], typer.Option()] = None,
             log: bool = typer.Option(False, "--log", "-l"),
             output: Annotated[Optional[str], typer.Option("--output", "-o")] = None,
             title: Annotated[Optional[str], typer.Option("--titel", "-t")] = None):

    raw = {
        "base_raw": base_raw,
        "zummarize_specific_raw": zummarize_specific_raw,
        "atr": {
            "colors": None if colors is None else shlex.split(colors),
            "markers": None if markers is None else shlex.split(markers),
            "cactus": cactus,
            "show_solved": show_solved,
            "center": center,
            "ymin": ymin,
            "xmin": xmin,
            "ymax": ymax,
            "xmax": xmax,
            "xlegend": xlegend,
            "ylegend": ylegend,
            "limit": limit,
            "log": log,
            "output": output,
            "title": title
        }
    }

    cfg = build_config(raw, PlotType.LinePlot)
    run_pipeline(cfg)
