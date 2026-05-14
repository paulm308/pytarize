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

    def transform_data(self, data: dict[str, pd.DataFrame]) -> list[tuple[str, list[float]]]:

        for folder_name in data.keys():
            data[folder_name] = data[folder_name][data[folder_name]["result"].isin([10, 20])]

        transformed = []
        for folder_name, values in data.items():
            tup = (folder_name, np.sort(values["time"].to_numpy()))
            transformed.append(tup)

        # sort the data so that the best run is first in the list
        transformed = sorted(transformed,
                             key=lambda x: x[1][len(x[1]) - 1],
                             reverse=True)

        return transformed

    def create_individual_plot_args(self, folder_name: str, values: list[float]):
        kwargs = {}
        kwargs["label"] = folder_name
        if "solver_style" in self.cfg.atr.keys() and folder_name in self.cfg.atr["solver_style"].keys():
            if "color" in self.cfg.atr["solver_style"][folder_name].keys():
                kwargs["color"] = self.cfg.atr["solver_style"][folder_name]["color"]
            if "marker" in self.cfg.atr["solver_style"][folder_name].keys():
                kwargs["marker"] = self.cfg.atr["solver_style"][folder_name]["marker"]
            if "label" in self.cfg.atr["solver_style"][folder_name].keys():
                kwargs["label"] = self.cfg.atr["solver_style"][folder_name]["label"]

        # show solved count in legend:
        if self.cfg.atr["show_solved"]:
            kwargs["label"] = f"{len(values)} {kwargs['label']}"
        xs = values
        ys = range(1, len(values) + 1)
        if self.cfg.atr["cactus"]:
            xs = range(1, len(values) + 1)
            ys = values
        args = (xs, ys)

        return {"args": args, "kwargs": kwargs}

    def create_legend_args(self):
        legend_kwargs = {}
        if self.cfg.atr["center"]:
            if self.cfg.atr["cactus"]:
                legend_kwargs["loc"] = "center left"
            else:
                legend_kwargs["loc"] = "center right"
        if self.cfg.atr["xlegend"] is not None or self.cfg.atr["ylegend"] is not None:
            xlegend = 0.5 if self.cfg.atr["xlegend"] is None else self.cfg.atr["xlegend"]
            ylegend = 0.5 if self.cfg.atr["ylegend"] is None else self.cfg.atr["ylegend"]
            legend_kwargs["bbox_to_anchor"] = (xlegend, ylegend)
        legend_kwargs["reverse"] = True
        return legend_kwargs

    def handle_axis_special(self, ax):
        ax.set_xlabel(self.cfg.atr["xlabel"])
        ax.set_ylabel(self.cfg.atr["ylabel"])

    def create_plot(self, data: list[tuple[str, list[float]]]):

        # handle latex text rendering
        utils.handle_latex(self.cfg)

        fig, ax = plt.subplots()

        # create style cycle (markers and colors)
        ax.set_prop_cycle(utils.create_style_cycle(self.cfg))

        for folder_name, values in data:
            plot_args = self.create_individual_plot_args(folder_name, values)
            ax.plot(*plot_args["args"], **plot_args["kwargs"])

        # draw limit line:
        if self.cfg.atr["limit"] is not None:
            plt.axhline(y=self.cfg.atr["limit"], color='blue', linestyle='-')

        # create legend:
        legend_kwargs = self.create_legend_args()
        ax.legend(**legend_kwargs)

        # handle axis scale and bounds
        utils.handle_axis(self.cfg, ax)
        self.handle_axis_special(ax)

        # title:
        if self.cfg.atr["title"] is not None:
            plt.title(self.cfg.atr["title"])

        plt.tight_layout()

        # save plot
        plt.savefig(self.cfg.atr["output"])
