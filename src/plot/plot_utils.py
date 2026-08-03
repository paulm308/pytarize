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


# create_individual_plot_args----------------------------------------------------------------------
def initialize_color(colors: list[str]) -> list[str]:
    """
    Changes colornames to tab:colornames.

    Parameters:
    colors (list[str]): List of colors given as name or hex.

    Returns:
    list[str]: transformed list of colors
    """
    for idx, color in enumerate(colors):
        if color[0] != "#":
            colors[idx] = f"tab:{color}"
    return colors


def create_style_cycle(cfg: CFG):
    """
    Creates a combined color and marker cycle. The number of colors and markers should be coprime.

    Parameters:
    cfg (CFG): The configuration.

    Returns:
    A cycler that yields color and marker pairs.
    """
    n = lcm(len(cfg.atr["colors"]), len(cfg.atr["markers"]))
    color_cycle = cfg.atr["colors"]
    combined = cycler(
        color=list(islice(cycle(color_cycle), n)),
        marker=list(islice(cycle(cfg.atr["markers"]), n)),
    )
    return combined


def add_solved_to_folder_name(data: list[tuple[str, list[float]]]) -> list[tuple[str, list[float]]]:
    """
    Adds the solved count to the front of the name of the folder.

    Parameters:
    data (list[tuple[str, list[float]]]): List of tuples of the folder name and the y values.

    Returns:
    list[tuple[str, list[float]]]: Transformed data.
    """
    for idx, tup in enumerate(data):
        folder_name, values = tup
        legend_label = f"{len(values)} {folder_name}"
        data[idx] = (legend_label, values)
    return data


def handle_marker(style):
    """
    Handles the advanced marker representation that also includes hollow markers.

    Parameters:
    style: An element of the style_cycle.

    Returns:
    tuple[str, bool]: The marker and a bool (hollow).
    """
    marker = style["marker"]
    hollow = False
    if not isinstance(style["marker"], str) and isinstance(style["marker"], list) and style["marker"] is not []:
        if isinstance(style["marker"][0], str):
            marker = style["marker"][0]
        if len(style["marker"]) >= 2 and isinstance(style["marker"][1], bool):
            hollow = style["marker"][1]
    return marker, hollow


# handle_axis -------------------------------------------------------------------------------------
def handle_axis_basic(cfg: CFG, ax):
    """
    This function handles axis styling that almost all plot types support. This function
    changes the scale of the axes and universal tick transformations such as setting the ticks, the rotation
    and handling tick_kwargs from the config.

    Parameters:
    cfg (CFG): The configuration.
    ax: The ax parameter from plt.subplots
    """
    if cfg.atr["xlog"]:
        ax.set_xscale("log")
    if cfg.atr["ylog"]:
        ax.set_yscale("log")
    set_ticks(cfg, ax)
    set_tick_rotation(cfg, ax)
    handle_tick_kwargs(cfg, ax)


def change_boundingbox_shape_to_square(ax):
    """
    Sets the aspect ratio of the axes to equal.

    Parameters:
    ax: The ax parameter from plt.subplots.
    """
    ax.set_aspect('equal', adjustable='box')


def disable_ticks_after_threshold(ax, threshold: tuple[float, float]):
    """
    Disables ticks after a threshold. This is used for the extend option.

    Parameters:
    ax: The ax parameter from plt.subplots.
    threshold (tuple[float, float]): The x and y-threshold.
    """
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
    """
    Changes the tick labels. This used for the plain notation and the TO label in the extend option.

    Parameters:
    ax: The ax parameter from plt.subplots.
    timeouts (Optional[tuple[float, float]]): The x and y-timeout values.
    label (Optional[str]): The new ticklabel.
    cfg (CFG): The configuration.
    """

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
    """
    Append a major tick to the list of major ticks.

    Parameters:
    p (tuple[float, float]): The position of the tick on the axes.
    ax: The ax parameter from plt.subplots.
    """
    xmajor_ticks = list(ax.get_xticks())
    ymajor_ticks = list(ax.get_yticks())

    xmajor_ticks.append(p[0])
    ymajor_ticks.append(p[1])

    ax.set_xticks(xmajor_ticks)
    ax.set_yticks(ymajor_ticks)


def set_ticks(cfg: CFG, ax):
    """
    Sets specific x and y-ticks.

    Parameters:
    cfg (CFG): The configuration.
    ax: The ax parameter from plt.subplots.
    """
    if "x_major_ticks" in cfg.atr.keys():
        ax.set_xticks(cfg.atr["x_major_ticks"])
    if "y_major_ticks" in cfg.atr.keys():
        ax.set_yticks(cfg.atr["y_major_ticks"])
    if "x_minor_ticks" in cfg.atr.keys():
        ax.set_xticks(cfg.atr["x_minor_ticks"], minor=True)
    if "y_minor_ticks" in cfg.atr.keys():
        ax.set_yticks(cfg.atr["y_minor_ticks"], minor=True)


def set_tick_rotation(cfg: CFG, ax):
    """
    Rotates all ticklabels on an axis.

    Parameters:
    cfg (CFG): The configuration.
    ax: The ax parameter from plt.subplots.
    """
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
    """
    Rotates all ticklabels on an axis.

    Parameters:
    cfg (CFG): The configuration.
    ax: The ax parameter from plt.subplots.
    """
    if "x_tick_kwargs" in cfg.atr.keys():
        ax.xaxis.set_tick_params(**cfg.atr["x_tick_kwargs"])
    if "y_tick_kwargs" in cfg.atr.keys():
        ax.yaxis.set_tick_params(**cfg.atr["y_tick_kwargs"])


# create_plot -------------------------------------------------------------------------------------
def create_solver_style(cfg, folder_names: list[str]):
    """
    Creates the solver_style dictionary that contains all the plot kwargs for a specific folder_name.
    This dict is generated from the colors and markers lists such as the universal_solver_style and specific_solver_style dictionaries.

    Parameters:
    cfg (CFG): The configuration.
    folder_names (list[str]): A list of the names of the folders that contain a zummary.
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


def handle_latex(cfg: CFG):
    """
    Handles the LaTeX text rendering.

    Parameters:
    cfg (CFG): The configuration.
    """
    plt.rcParams['text.usetex'] = cfg.atr["latex"]
    plt.rcParams["font.family"] = cfg.atr["font_family"]
    if cfg.atr["latex_preamble"] is not None:
        plt.rcParams["text.latex.preamble"] = cfg.atr["latex_preamble"]


def plot_lines(data, ax):
    """
    Plots the lines given in indicator_lines in the config.

    data: indicator_lines.
    ax: The ax parameter from plt.subplots.
    """
    for line in data:
        ax.axline(*line["axline_args"], **line["axline_kwargs"])


def plot_line_segments(data, ax):
    """
    Plots the lines given in indicator_line_segments in the config.

    data: indicator_line_segments.
    ax: The ax parameter from plt.subplots.
    """
    for lineseg in data:
        ax.plot(*lineseg["plot_args"], **lineseg["plot_kwargs"])


def create_legend_args(cfg: CFG):
    """
    Creates the keyword arguments for ax.legend.
    This function sets the position and style of the legend.

    Parameters:
    cfg (CFG): The configuration.

    Returns:
    dict: The keyword arguments for ax.legend.
    """
    legend_kwargs = {}
    if cfg.atr["center"]:
        legend_kwargs["loc"] = "center right"
    elif cfg.atr["legendloc"] is not None:
        legend_kwargs["loc"] = cfg.atr["legendloc"]
    if cfg.atr["xlegend"] is not None or cfg.atr["ylegend"] is not None:
        xlegend = 0.5 if cfg.atr["xlegend"] is None else cfg.atr["xlegend"]
        ylegend = 0.5 if cfg.atr["ylegend"] is None else cfg.atr["ylegend"]
        legend_kwargs["loc"] = "center"
        legend_kwargs["bbox_to_anchor"] = (xlegend, ylegend)
    legend_kwargs["reverse"] = True
    return legend_kwargs
