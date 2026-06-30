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
def base(zummarizepath: Annotated[Optional[str], typer.Option("--zummarizepath", "--zrp", help="path to zummarize script")] = None,
         logpaths: Annotated[Optional[str], typer.Option("--logpaths", "--lps", help="list of paths that lead to folders containing the logs")] = None,
         rlogpaths: Annotated[Optional[str], typer.Option("--rlogpaths", "--rlps", help="list of root paths that are recursively searched for log folders")] = None,
         configpaths: Annotated[Optional[str], typer.Option("--configpaths", "--cps", help="list of paths that lead to config files")] = None,
         save_config: Annotated[Optional[str], typer.Option("--save-config", "--sc", help="Saves a config at the given possition and name that contains the state of all arguments")] = None,
         verbose: Annotated[Optional[int], typer.Option("-v", help="increase verbose level (maximum 3, default 0)")] = None,
         force: bool = typer.Option(False, "--force", "-f", help="recompute zummaries (do not read '<dir>/zummary' files)"),
         ignore: bool = typer.Option(False, "--ignore", "-i", help="ignore mismatching limits and bounds"),
         just: bool = typer.Option(False, "--just", "-j", help="assume terminated are just solved (unsat)"),
         no_warnings: bool = typer.Option(False, "--no-warnings", "-n", help="disables warnings"),
         all: bool = typer.Option(False, "--all", "-a", help="report all column and rows (even with zero entries)"),
         sat: bool = typer.Option(False, "--sat", "-s", help="report goes over satisfiable instances only"),
         unsat: bool = typer.Option(False, "--unsat", "-u", help="report goes over unsatisfiable instances only"),
         deep: bool = typer.Option(False, "--deep", "-d", help="report goes over unsolved instances only (sorted by deep)"),
         rank: bool = typer.Option(False, "--rank", "-r", help="print number of times benchmark has been solved"),
         unsolved: bool = typer.Option(False, "--unsolved", help="print unsolved (never solved) instances"),
         solved: bool = typer.Option(False, "--solved", help="print all at least once solved instances"),
         filter: bool = typer.Option(False, "--filter", help="filter out solved in comparison"),
         cmp: bool = typer.Option(False, "--cmp", help="compare two runs"),
         no_write: bool = typer.Option(False, "--no-write", help="do not write generated zummaries"),
         no_bounds: bool = typer.Option(False, "--no-bounds", help="do not print bounds"),
         force_real: bool = typer.Option(False, "--force-real", help="force real time zummaries"),
         force_time: bool = typer.Option(False, "--force-time", help="force process time zummaries")):

    base_raw["zummarize_path"] = zummarizepath
    base_raw["log_paths"] = None if logpaths is None else shlex.split(logpaths)
    base_raw["r_log_paths"] = None if rlogpaths is None else shlex.split(rlogpaths)
    base_raw["config_paths"] = None if configpaths is None else shlex.split(configpaths)
    base_raw["save_config"] = save_config

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
def lineplot(colors: Annotated[Optional[str], typer.Option("--colors", help="list of colors (hex or name in color table)")] = None,
             markers: Annotated[Optional[str], typer.Option("--markers", help="list of markers used by marker argument in plt.plot")] = None,
             hollow: bool = typer.Option(False, "--hollow", help="create hollow markers"),
             cactus: bool = typer.Option(False, "--cactus", help="generate cactus plot (cdf is defaut)"),
             show_solved: bool = typer.Option(False, "--show-solved", help="show solved count in legend"),
             center: bool = typer.Option(False, "--center", help="center legend vertically"),
             legendloc: Annotated[Optional[str], typer.Option("--legendloc", help="set the location of the legend. ('upper left', 'upper center', 'upper right', 'center ...' 'lower ...'")] = None,
             ymin: Annotated[Optional[float], typer.Option("--ymin", help="minimum y-axis value")] = None,
             xmin: Annotated[Optional[float], typer.Option("--xmin", help="minimum x-axis value")] = None,
             ymax: Annotated[Optional[float], typer.Option("--ymax", help="maximum y-axis value")] = None,
             xmax: Annotated[Optional[float], typer.Option("--xmax", help="maximum x-axis value")] = None,
             xlegend: Annotated[Optional[float], typer.Option("--xlegend", help="x position of the top left corner of the legend (values between 0 and 1)")] = None,
             ylegend: Annotated[Optional[float], typer.Option("--ylegend", help="y position of the top left corner of the legend (values between 0 and 1)")] = None,
             limit: Annotated[Optional[float], typer.Option("--limit", help="plot a horizontal line at the given y value")] = None,
             lines: bool = typer.Option(False, "--lines", help="Plot the indicator lines specified by 'indicator_lines' in the config"),
             line_segments: bool = typer.Option(False, "--line-segments", help="Plot the indicator line segments specified by 'indicator_line_segments' in the config. This can also be used to create small plots."),
             grid: bool = typer.Option(False, "--grid", help="Plot the grid specified by 'grid_kwargs' in the config"),
             xlog: bool = typer.Option(False, "--xlog", help="change x scale from linear to log"),
             ylog: bool = typer.Option(False, "--ylog", help="change y scale from linear to log"),
             xlabel: Annotated[Optional[str], typer.Option("--xlabel", help="x-axis label")] = None,
             ylabel: Annotated[Optional[str], typer.Option("--ylabel", help="y-axis label")] = None,
             plain: bool = typer.Option(False, "--plain", help="Disable scientific notation"),
             square_box: bool = typer.Option(False, "--square-box", help="set equal aspect ratio"),
             output: Annotated[Optional[str], typer.Option("--output", "-o", help="location, name and type of the output")] = None,
             title: Annotated[Optional[str], typer.Option("--titel", "-t", help="title on top of the plot")] = None,
             latex: bool = typer.Option(False, "--latex", help="Enable latex text rendering."),
             font_family: Annotated[Optional[str], typer.Option("--font-family", help="Change latex font-family, default is 'serif', options: 'serif', 'sans-serif', 'monospace', 'cursive'...")] = None,
             latex_preamble: Annotated[Optional[str], typer.Option("--latex-preamble", help="Use this to import packages, example: '\\usepackage{helvet}\\usepackage{sfmath}'")] = None,
             create_solver_style: bool = typer.Option(False, "--create-solver-style", "--css", help="Generates the solver_style dictionary in the config. --save-config needs to be specified as well to save the dict in the config.")):

    raw = {
        "base_raw": base_raw,
        "zummarize_specific_raw": zummarize_specific_raw,
        "atr": {
            "colors": None if colors is None else shlex.split(colors),
            "markers": None if markers is None else shlex.split(markers),
            "hollow": hollow,
            "cactus": cactus,
            "show_solved": show_solved,
            "center": center,
            "legendloc": legendloc,
            "ymin": ymin,
            "xmin": xmin,
            "ymax": ymax,
            "xmax": xmax,
            "xlegend": xlegend,
            "ylegend": ylegend,
            "limit": limit,
            "lines": lines,
            "line_segments": line_segments,
            "grid": grid,
            "xlog": xlog,
            "ylog": ylog,
            "xlabel": xlabel,
            "ylabel": ylabel,
            "plain": plain,
            "square_box": square_box,
            "output": output,
            "title": title,
            "latex": latex,
            "font_family": font_family,
            "latex_preamble": latex_preamble,
            "create_solver_style": create_solver_style
        }
    }

    cfg = build_config(raw, PlotType.LinePlot)
    run_pipeline(cfg)


@app.command()
def scatterplot(colors: Annotated[Optional[str], typer.Option("--colors", help="list of colors (hex or name in color table)")] = None,
                markers: Annotated[Optional[str], typer.Option("--markers", help="list of markers used by marker argument in plt.plot")] = None,
                hollow: bool = typer.Option(False, "--hollow", help="create hollow markers"),
                show_solved: bool = typer.Option(False, "--show-solved", help="show solved count in legend"),
                center: bool = typer.Option(False, "--center", help="center legend vertically"),
                legendloc: Annotated[Optional[str], typer.Option("--legendloc", help="set the location of the legend. ('upper left', 'upper center', 'upper right', 'center ...' 'lower ...'")] = None,
                ymin: Annotated[Optional[float], typer.Option("--ymin", help="minimum y-axis value")] = None,
                xmin: Annotated[Optional[float], typer.Option("--xmin", help="minimum x-axis value")] = None,
                ymax: Annotated[Optional[float], typer.Option("--ymax", help="maximum y-axis value")] = None,
                xmax: Annotated[Optional[float], typer.Option("--xmax", help="maximum x-axis value")] = None,
                xlegend: Annotated[Optional[float], typer.Option("--xlegend", help="x position of the top left corner of the legend (values between 0 and 1)")] = None,
                ylegend: Annotated[Optional[float], typer.Option("--ylegend", help="y position of the top left corner of the legend (values between 0 and 1)")] = None,
                limit: bool = typer.Option(False, "--limit", help="plot the timeout lines at the timeout value in the zummary"),
                lines: bool = typer.Option(False, "--lines", help="Plot the indicator lines specified by 'indicator_lines' in the config"),
                line_segments: bool = typer.Option(False, "--line-segments", help="Plot the indicator line segments specified by 'indicator_line_segments' in the config. This can also be used to create small plots."),
                grid: bool = typer.Option(False, "--grid", help="Plot the grid specified by 'grid_kwargs' in the config"),
                extend: Annotated[Optional[float], typer.Option("--extend", help="Enable the extended mode that scales the plot down by the input value and adds a timeout line")] = None,
                xlog: bool = typer.Option(False, "--xlog", help="change x scale from linear to log"),
                ylog: bool = typer.Option(False, "--ylog", help="change y scale from linear to log"),
                xlabel: Annotated[Optional[str], typer.Option("--xlabel", help="x-axis label")] = None,
                ylabel: Annotated[Optional[str], typer.Option("--ylabel", help="y-axis label")] = None,
                plain: bool = typer.Option(False, "--plain", help="Disable scientific notation"),
                square_box: bool = typer.Option(False, "--square-box", help="set equal aspect ratio"),
                output: Annotated[Optional[str], typer.Option("--output", "-o", help="location, name and type of the output")] = None,
                title: Annotated[Optional[str], typer.Option("--titel", "-t", help="title on top of the plot")] = None,
                latex: bool = typer.Option(False, "--latex", help="Enable latex text rendering."),
                font_family: Annotated[Optional[str], typer.Option("--font-family", help="Change latex font-family, default is 'serif', options: 'serif', 'sans-serif', 'monospace', 'cursive'...")] = None,
                latex_preamble: Annotated[Optional[str], typer.Option("--latex-preamble", help="Use this to import packages, example: '\\usepackage{helvet}\\usepackage{sfmath}'")] = None):

    raw = {
        "base_raw": base_raw,
        "zummarize_specific_raw": zummarize_specific_raw,
        "atr": {
            "colors": None if colors is None else shlex.split(colors),
            "markers": None if markers is None else shlex.split(markers),
            "hollow": hollow,
            "show_solved": show_solved,
            "center": center,
            "legendloc": legendloc,
            "ymin": ymin,
            "xmin": xmin,
            "ymax": ymax,
            "xmax": xmax,
            "xlegend": xlegend,
            "ylegend": ylegend,
            "limit": limit,
            "lines": lines,
            "line_segments": line_segments,
            "grid": grid,
            "extend": extend,
            "xlog": xlog,
            "ylog": ylog,
            "xlabel": xlabel,
            "ylabel": ylabel,
            "plain": plain,
            "square_box": square_box,
            "output": output,
            "title": title,
            "latex": latex,
            "font_family": font_family,
            "latex_preamble": latex_preamble
        }
    }

    cfg = build_config(raw, PlotType.ScatterPlot)
    run_pipeline(cfg)


@app.command()
def combinedplot(unique: bool = typer.Option(False, "--unique"),
                 stable: bool = typer.Option(False, "--stable"),
                 horse: bool = typer.Option(False, "--horse"),
                 sota: bool = typer.Option(False, "--sota"),
                 relative: bool = typer.Option(False, "--relative"),
                 time: bool = typer.Option(False, "--time", help="Use time instead of real (real is default)"),
                 colors: Annotated[Optional[str], typer.Option("--colors", help="list of colors (hex or name in color table)")] = None,
                 markers: Annotated[Optional[str], typer.Option("--markers", help="list of markers used by marker argument in plt.plot")] = None,
                 hollow: bool = typer.Option(False, "--hollow", help="create hollow markers"),
                 show_solved: bool = typer.Option(False, "--show-solved", help="show solved count in legend"),
                 center: bool = typer.Option(False, "--center", help="center legend vertically"),
                 legendloc: Annotated[Optional[str], typer.Option("--legendloc", help="set the location of the legend. ('upper left', 'upper center', 'upper right', 'center ...' 'lower ...'")] = None,
                 ymin: Annotated[Optional[float], typer.Option("--ymin", help="minimum y-axis value")] = None,
                 xmin: Annotated[Optional[float], typer.Option("--xmin", help="minimum x-axis value")] = None,
                 ymax: Annotated[Optional[float], typer.Option("--ymax", help="maximum y-axis value")] = None,
                 xmax: Annotated[Optional[float], typer.Option("--xmax", help="maximum x-axis value")] = None,
                 xlegend: Annotated[Optional[float], typer.Option("--xlegend", help="x position of the top left corner of the legend (values between 0 and 1)")] = None,
                 ylegend: Annotated[Optional[float], typer.Option("--ylegend", help="y position of the top left corner of the legend (values between 0 and 1)")] = None,
                 limit: Annotated[Optional[float], typer.Option("--limit", help="plot a horizontal line at the given y value")] = None,
                 lines: bool = typer.Option(False, "--lines", help="Plot the indicator lines specified by 'indicator_lines' in the config"),
                 line_segments: bool = typer.Option(False, "--line-segments", help="Plot the indicator line segments specified by 'indicator_line_segments' in the config. This can also be used to create small plots."),
                 grid: bool = typer.Option(False, "--grid", help="Plot the grid specified by 'grid_kwargs' in the config"),
                 xlog: bool = typer.Option(False, "--xlog", help="change x scale from linear to log"),
                 ylog: bool = typer.Option(False, "--ylog", help="change y scale from linear to log"),
                 xlabel: Annotated[Optional[str], typer.Option("--xlabel", help="x-axis label")] = None,
                 ylabel: Annotated[Optional[str], typer.Option("--ylabel", help="y-axis label")] = None,
                 plain: bool = typer.Option(False, "--plain", help="Disable scientific notation"),
                 square_box: bool = typer.Option(False, "--square-box", help="set equal aspect ratio"),
                 output: Annotated[Optional[str], typer.Option("--output", "-o", help="location, name and type of the output")] = None,
                 title: Annotated[Optional[str], typer.Option("--titel", "-t", help="title on top of the plot")] = None,
                 latex: bool = typer.Option(False, "--latex", help="Enable latex text rendering."),
                 font_family: Annotated[Optional[str], typer.Option("--font-family", help="Change latex font-family, default is 'serif', options: 'serif', 'sans-serif', 'monospace', 'cursive'...")] = None,
                 latex_preamble: Annotated[Optional[str], typer.Option("--latex-preamble", help="Use this to import packages, example: '\\usepackage{helvet}\\usepackage{sfmath}'")] = None,
                 create_solver_style: bool = typer.Option(False, "--create-solver-style", "--css", help="Generates the solver_style dictionary in the config. --save-config needs to be specified as well to save the dict in the config.")):

    raw = {
        "base_raw": base_raw,
        "zummarize_specific_raw": zummarize_specific_raw,
        "atr": {
            "unique": unique,
            "stable": stable,
            "horse": horse,
            "sota": sota,
            "relative": relative,
            "time": time,
            "colors": None if colors is None else shlex.split(colors),
            "markers": None if markers is None else shlex.split(markers),
            "hollow": hollow,
            "show_solved": show_solved,
            "center": center,
            "legendloc": legendloc,
            "ymin": ymin,
            "xmin": xmin,
            "ymax": ymax,
            "xmax": xmax,
            "xlegend": xlegend,
            "ylegend": ylegend,
            "limit": limit,
            "lines": lines,
            "line_segments": line_segments,
            "grid": grid,
            "xlog": xlog,
            "ylog": ylog,
            "xlabel": xlabel,
            "ylabel": ylabel,
            "plain": plain,
            "square_box": square_box,
            "output": output,
            "title": title,
            "latex": latex,
            "font_family": font_family,
            "latex_preamble": latex_preamble,
            "create_solver_style": create_solver_style
        }
    }

    cfg = build_config(raw, PlotType.CombinedPlot)
    run_pipeline(cfg)

# +---------------------+
# | Add new plot option |
# +---------------------+
