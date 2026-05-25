from src.core.configuration_data import CFG
from matplotlib import pyplot as plt
from cycler import cycler
from math import lcm
from itertools import cycle, islice
from matplotlib.ticker import ScalarFormatter
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


def change_tick_notation_to_plain(ax):
    formatter = ScalarFormatter()
    formatter.set_scientific(False)
    formatter.set_useOffset(False)
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)


def plot_lines(data, ax):
    for line in data:
        ax.axline(*line["axline_args"], **line["axline_kwargs"])
