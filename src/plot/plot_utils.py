from src.core.configuration_data import CFG
from src.cli.dictmerger import merge_dicts
from matplotlib import pyplot as plt
from cycler import cycler
from math import lcm
from itertools import cycle, islice
from matplotlib.ticker import FuncFormatter
import numpy as np
from typing import Optional
from matplotlib.markers import MarkerStyle


def initialize_color(colors: list[str]) -> list[str]:
    for idx, color in enumerate(colors):
        if color[0] != "#":
            colors[idx] = f"tab:{color}"
    return colors


def create_style_cycle(cfg: CFG):
    # create marker and color cycle:
    n = lcm(len(cfg.atr["colors"]), len(cfg.atr["markers"]))
    color_cycle = cfg.atr["colors"]
    combined = cycler(
        color=list(islice(cycle(color_cycle), n)),
        marker=list(islice(cycle(cfg.atr["markers"]), n)),
    )
    return combined


def add_solved_to_folder_name(data: list[tuple[str, list[float]]]) -> list[tuple[str, list[float]]]:
    for idx, tup in enumerate(data):
        folder_name, values = tup
        legend_label = f"{len(values)} {folder_name}"
        data[idx] = (legend_label, values)
    return data


def handle_latex(cfg: CFG):
    plt.rcParams['text.usetex'] = cfg.atr["latex"]
    plt.rcParams["font.family"] = cfg.atr["font_family"]
    if cfg.atr["latex_preamble"] is not None:
        plt.rcParams["text.latex.preamble"] = cfg.atr["latex_preamble"]


def handle_axis_basic(cfg: CFG, ax):
    if cfg.atr["xlog"]:
        ax.set_xscale("log")
    if cfg.atr["ylog"]:
        ax.set_yscale("log")
    set_ticks(cfg, ax)
    set_tick_rotation(cfg, ax)
    handle_tick_kwargs(cfg, ax)


def change_boundingbox_shape_to_square(ax):
    ax.set_aspect('equal', adjustable='box')


def plot_lines(data, ax):
    for line in data:
        ax.axline(*line["axline_args"], **line["axline_kwargs"])


def plot_line_segments(data, ax):
    for lineseg in data:
        ax.plot(*lineseg["plot_args"], **lineseg["plot_kwargs"])


def disable_ticks_after_threshold(ax, threshold: tuple[float, float]):
    xmajor_ticks = list(ax.get_xticks())
    ymajor_ticks = list(ax.get_yticks())

    if threshold[0] not in xmajor_ticks:
        xmajor_ticks.append(threshold[0])
    if threshold[1] not in ymajor_ticks:
        ymajor_ticks.append(threshold[1])

    ax.set_xticks([t for t in xmajor_ticks if t <= threshold[0]])
    ax.set_yticks([t for t in ymajor_ticks if t <= threshold[1]])

    xminor_ticks = [
        t for t in ax.xaxis.get_minorticklocs()
        if t <= threshold[0]
    ]

    yminor_ticks = [
        t for t in ax.yaxis.get_minorticklocs()
        if t <= threshold[1]
    ]

    ax.set_xticks(xminor_ticks, minor=True)
    ax.set_yticks(yminor_ticks, minor=True)


def change_tick_notation_label(ax, timeouts: Optional[tuple[float, float]], label: Optional[str], cfg: CFG):

    def formatter(y, pos):
        if timeouts is not None and np.isclose(y, timeouts[1]) and cfg.atr["extend"] is not None and label is not None:
            return label
        elif cfg.atr["plain"]:
            return f"{y:g}"
        else:
            return y

    ax.xaxis.set_major_formatter(FuncFormatter(formatter))
    ax.yaxis.set_major_formatter(FuncFormatter(formatter))


def append_major_tick(p: tuple[float, float], ax):
    xmajor_ticks = list(ax.get_xticks())
    ymajor_ticks = list(ax.get_yticks())

    xmajor_ticks.append(p[0])
    ymajor_ticks.append(p[1])

    ax.set_xticks(xmajor_ticks)
    ax.set_yticks(ymajor_ticks)


def set_ticks(cfg: CFG, ax):
    if "x_major_ticks" in cfg.atr.keys():
        ax.set_xticks(cfg.atr["x_major_ticks"])
    if "y_major_ticks" in cfg.atr.keys():
        ax.set_yticks(cfg.atr["y_major_ticks"])
    if "x_minor_ticks" in cfg.atr.keys():
        ax.set_xticks(cfg.atr["x_minor_ticks"], minor=True)
    if "y_minor_ticks" in cfg.atr.keys():
        ax.set_yticks(cfg.atr["y_minor_ticks"], minor=True)


def set_tick_rotation(cfg: CFG, ax):
    if "x_tick_rotation" in cfg.atr.keys():
        for label in ax.get_xticklabels():
            label.set_rotation(cfg.atr["x_tick_rotation"])
            label.set_verticalalignment('center')
            label.set_horizontalalignment('center')
    if "y_tick_rotation" in cfg.atr.keys():
        for label in ax.get_yticklabels():
            label.set_rotation(cfg.atr["y_tick_rotation"])
            label.set_verticalalignment('center')
            label.set_horizontalalignment('center')


def handle_tick_kwargs(cfg: CFG, ax):
    if "x_tick_kwargs" in cfg.atr.keys():
        ax.xaxis.set_tick_params(**cfg.atr["x_tick_kwargs"])
    if "y_tick_kwargs" in cfg.atr.keys():
        ax.yaxis.set_tick_params(**cfg.atr["y_tick_kwargs"])


def create_solver_style(cfg, folder_names: list[str]):
    """
    Creates the solver_style dictionary that contains all the plot kwargs for a specific folder_name.
    This dict is generated from the colors and markers lists such as the universal_solver_style and specific_solver_style dictionarys.
    """
    solver_style = {}
    if "solver_style" in cfg.atr.keys() and cfg.atr["solver_style"] is not None:
        solver_style = cfg.atr["solver_style"]

    style_cycle = cycle(create_style_cycle(cfg))

    # create folder order:
    order = folder_names
    if cfg.atr["order"] and "specific_solver_style" in cfg.atr.keys() and cfg.atr["specific_solver_style"] is not None:
        order = list(cfg.atr["specific_solver_style"].keys())
        order += [folder_name for folder_name in folder_names if folder_name not in order]

    for folder_name in order:
        kwargs = {}
        style = next(style_cycle)
        kwargs["color"] = style["color"]

        # handle marker style:
        if isinstance(style["marker"], str):
            kwargs["marker"] = style["marker"]
        elif isinstance(style["marker"], list) and style["marker"] is not []:
            if isinstance(style["marker"][0], str):
                kwargs["marker"] = style["marker"][0]
            if len(style["marker"]) >= 2 and isinstance(style["marker"][1], bool):
                kwargs["hollow"] = style["marker"][1]

        # initialize label:
        if (folder_name in solver_style.keys() and
            solver_style[folder_name] is not None and
            "label" in solver_style[folder_name].keys() and
            solver_style[folder_name]["label"] is not None):
                
            kwargs["label"] = solver_style[folder_name]["label"]
        else:
            kwargs["label"] = folder_name

        # apply universal styling:
        if "universal_solver_style" in cfg.atr.keys() and cfg.atr["universal_solver_style"] is not None:
            kwargs = merge_dicts(kwargs, cfg.atr["universal_solver_style"], additive=False)

        # apply specific styling:
        if ("specific_solver_style" in cfg.atr.keys() and
            cfg.atr["specific_solver_style"] is not None and
            folder_name in cfg.atr["specific_solver_style"].keys() and
            cfg.atr["specific_solver_style"][folder_name] is not None):

            kwargs = merge_dicts(kwargs, cfg.atr["specific_solver_style"][folder_name], additive=False)

        # create hollow markers:
        if "hollow" in kwargs.keys():
            if (kwargs["hollow"] is not None and
                kwargs["hollow"] is True and
                kwargs["marker"] in MarkerStyle.filled_markers):

                kwargs["markeredgecolor"] = kwargs["color"]
                kwargs["markerfacecolor"] = "none"
            kwargs.pop("hollow", None)

        # apply kwargs on previous solver_style to form final solver style:
        if folder_name in solver_style.keys() and solver_style[folder_name] is not None:
            solver_style[folder_name] = merge_dicts(solver_style[folder_name], kwargs, additive=False)
        else:
            solver_style[folder_name] = kwargs

    cfg.atr["solver_style"] = solver_style
