from src.core.configuration_data import CFG
from matplotlib import pyplot as plt
from cycler import cycler
from math import lcm
from itertools import cycle, islice


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


def handle_axis(cfg: CFG):
    if cfg.atr["xlog"]:
        plt.xscale("log")
    if cfg.atr["ylog"]:
        plt.yscale("log")
    plt.xlim(cfg.atr["xmin"], cfg.atr["xmax"])
    plt.ylim(cfg.atr["ymin"], cfg.atr["ymax"])
