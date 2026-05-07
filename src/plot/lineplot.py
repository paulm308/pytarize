from src.plot.baseplot import BasePlot
from src.core.configuration_data import CFG
import src.plot.plot_utils as utils
import pandas as pd
import numpy as np
from typing import Generic, TypeVar
from matplotlib import pyplot as plt
from cycler import cycler
from math import lcm
from itertools import cycle, islice


class LinePlot(BasePlot):

    def transform_data(self, data: dict[str, pd.DataFrame], cfg: CFG) -> list[tuple[str, list[float]]]:
        transformed = []
        for folder_name, values in data.items():
            tup = (folder_name, np.sort(values["time"].to_numpy()))
            transformed.append(tup)

        # sort the data so that the best run is first in the list
        transformed = sorted(transformed,
                             key=lambda x: x[1][len(x[1]) - 1],
                             reverse=True)

        return transformed

    def create_style_cycle(self, cfg: CFG):
        # create marker and color cycle:
        n = lcm(len(cfg.atr["colors"]), len(cfg.atr["markers"]))
        color_cycle = utils.initialize_color(cfg.atr["colors"])
        combined = cycler(
            color=list(islice(cycle(reversed(color_cycle)), n)),
            marker=list(islice(cycle(reversed(cfg.atr["markers"])), n)),
        )
        return combined

    def create_individual_plot_args(self, folder_name: str, values: list[float], cfg: CFG):
        kwargs = {}
        kwargs["label"] = folder_name
        if "solver_style" in cfg.atr.keys() and folder_name in cfg.atr["solver_style"].keys():
            if "color" in cfg.atr["solver_style"][folder_name].keys():
                kwargs["color"] = cfg.atr["solver_style"][folder_name]["color"]
            if "marker" in cfg.atr["solver_style"][folder_name].keys():
                kwargs["marker"] = cfg.atr["solver_style"][folder_name]["marker"]
            if "label" in cfg.atr["solver_style"][folder_name].keys():
                kwargs["label"] = cfg.atr["solver_style"][folder_name]["label"]

        # show solved count in legend:
        if cfg.atr["show_solved"]:
            kwargs["label"] = f"{len(values)} {kwargs['label']}"
        xs = values
        ys = range(1, len(values) + 1)
        if cfg.atr["cactus"]:
            xs = range(1, len(values) + 1)
            ys = values
        args = (xs, ys)

        return {"args": args, "kwargs": kwargs}

    def create_legend_args(self, cfg: CFG):
        legend_kwargs = {}
        if cfg.atr["center"]:
            if cfg.atr["cactus"]:
                legend_kwargs["loc"] = "center left"
            else:
                legend_kwargs["loc"] = "center right"
        if cfg.atr["xlegend"] is not None or cfg.atr["ylegend"] is not None:
            xlegend = 0.5 if cfg.atr["xlegend"] is None else cfg.atr["xlegend"]
            ylegend = 0.5 if cfg.atr["ylegend"] is None else cfg.atr["ylegend"]
            legend_kwargs["bbox_to_anchor"] = (xlegend, ylegend)
        legend_kwargs["reverse"] = True
        return legend_kwargs

    def handle_axis(self, cfg: CFG):
        if cfg.atr["xlog"]:
            plt.xscale("log")
        if cfg.atr["ylog"]:
            plt.yscale("log")
        plt.xlim(cfg.atr["xmin"], cfg.atr["xmax"])
        plt.ylim(cfg.atr["ymin"], cfg.atr["ymax"])

    def create_plot(self, data: list[tuple[str, list[float]]], cfg: CFG):

        plt.rcParams['text.usetex'] = cfg.atr["latex"]
        plt.rcParams["font.family"] = cfg.atr["font_family"]
        if cfg.atr["latex_preamble"] is not None:
            plt.rcParams["text.latex.preamble"] = cfg.atr["latex_preamble"]

        fig, ax = plt.subplots()

        ax.set_prop_cycle(self.create_style_cycle(cfg))

        for folder_name, values in data:
            plot_args = self.create_individual_plot_args(folder_name, values, cfg)
            ax.plot(*plot_args["args"], **plot_args["kwargs"])

        # draw limit line:
        if cfg.atr["limit"] is not None:
            plt.axhline(y=cfg.atr["limit"], color='blue', linestyle='-')

        # create legend:
        legend_kwargs = self.create_legend_args(cfg)
        ax.legend(**legend_kwargs)

        self.handle_axis(cfg)

        # title:
        if cfg.atr["title"] is not None:
            plt.title(cfg.atr["title"])

        plt.tight_layout()

        # save plot
        plt.savefig(cfg.atr["output"])
