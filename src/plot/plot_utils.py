from src.core.configuration_data import CFG
from matplotlib import pyplot as plt
from cycler import cycler
from math import lcm
from itertools import cycle, islice
from matplotlib.ticker import FuncFormatter
import numpy as np
from typing import Optional


def initialize_color(colors: list[str]) -> list[str]:
    for idx, color in enumerate(colors):
        if color[0] != "#":
            colors[idx] = f"tab:{color}"
    return colors


def create_style_cycle(cfg: CFG):
    # create marker and color cycle:
    n = lcm(len(cfg.atr["colors"]), len(cfg.atr["markers"]))
    color_cycle = initialize_color(cfg.atr["colors"])
    combined = cycler(
        color=list(islice(cycle(reversed(color_cycle)), n)),
        marker=list(islice(cycle(reversed(cfg.atr["markers"])), n)),
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
