from src.plot.baseplot import BasePlot
from src.core.save_data import save_solver_style
from typing import Optional
import src.plot.plot_utils as utils
import pandas as pd
import numpy as np
import matplotlib as mat
from matplotlib import pyplot as plt
from itertools import cycle, islice
from matplotlib.markers import MarkerStyle
mat.use("Agg")


class LinePlot(BasePlot):

    def transform_data(self, data: dict[str, pd.DataFrame]) -> list[tuple[str, list[float], list[float], Optional[int]]]:
        """
        Transforms the data in to a cdf or cactus representation.
        """

        for folder_name in data.keys():
            data[folder_name] = data[folder_name][data[folder_name]["result"].isin([10, 20])]

        transformed = []
        for folder_name, values in data.items():
            tup = (folder_name, np.sort(values["time"].to_numpy()), list(range(1, len(values) + 1)), len(values))
            transformed.append(tup)

        # sort the data so that the best run is first in the list
        transformed = sorted(transformed,
                             key=lambda x: len(x[1]))

        if self.cfg.atr["cactus"]:
            transformed = [(tup[0], tup[2], tup[1], tup[3]) for tup in transformed]

        return transformed

    def create_individual_plot_args(self, folder_name: str, style_cycle, xs: list[float], ys: list[float], num_in_label: Optional[int]):
        """
        Creates the arguments and keywordarguments used by plt.plot.
        This affects the styling of the individual plot lines such as the name in the legend
        """
        kwargs = {}

        style = next(style_cycle)
        color = style["color"]
        kwargs["label"] = folder_name

        kwargs["marker"], hollow = utils.handle_marker(style)

        # apply solver_style styling
        if "solver_style" in self.cfg.atr.keys() and folder_name in self.cfg.atr["solver_style"].keys():
            if "color" in self.cfg.atr["solver_style"][folder_name].keys():
                color = self.cfg.atr["solver_style"][folder_name]["color"]
                self.cfg.atr["solver_style"][folder_name].pop("color", None)
            if "marker" in self.cfg.atr["solver_style"][folder_name].keys():
                kwargs["marker"] = self.cfg.atr["solver_style"][folder_name]["marker"]
                self.cfg.atr["solver_style"][folder_name].pop("marker", None)
            if "label" in self.cfg.atr["solver_style"][folder_name].keys():
                kwargs["label"] = self.cfg.atr["solver_style"][folder_name]["label"]
                self.cfg.atr["solver_style"][folder_name].pop("label", None)
            kwargs.update(self.cfg.atr["solver_style"][folder_name])

        # create holow markers
        if kwargs["marker"] in MarkerStyle.filled_markers and (hollow or self.cfg.atr["hollow"]):
            kwargs["markeredgecolor"] = color
            kwargs["markerfacecolor"] = "none"
        kwargs["color"] = color

        # show solved count in legend:
        if self.cfg.atr["show_solved"] and num_in_label is not None:
            kwargs["label"] = f"{num_in_label} {kwargs['label']}"
        args = (xs, ys)

        return {"args": args, "kwargs": kwargs}

    def handle_axis(self, ax):
        utils.handle_axis_basic(self.cfg, ax)
        ax.set_xlim(self.cfg.atr["xmin"], self.cfg.atr["xmax"])
        ax.set_ylim(self.cfg.atr["ymin"], self.cfg.atr["ymax"])
        if self.cfg.atr["square_box"]:
            utils.change_boundingbox_shape_to_square(ax)
        ax.set_xlabel(self.cfg.atr["xlabel"])
        ax.set_ylabel(self.cfg.atr["ylabel"])
        if self.cfg.atr["plain"]:
            utils.change_tick_notation_label(ax, None, None, self.cfg)

    def create_plot(self, data: list[tuple[str, list[float], list[float], Optional[int]]]):

        if self.cfg.atr["create_solver_style"]:
            utils.create_solver_style(self. cfg, folder_names=list(reversed([tup[0] for tup in data])))
            save_solver_style(self.cfg)

        # handle latex text rendering
        utils.handle_latex(self.cfg)

        subplots_kwargs = {}
        if "subplots_kwargs" in self.cfg.atr.keys():
            subplots_kwargs = self.cfg.atr["subplots_kwargs"]

        fig, ax = plt.subplots(**subplots_kwargs)

        # create style cycle (markers and colors)
        style_cycle = reversed(list(islice(cycle(utils.create_style_cycle(self.cfg)), len(data))))

        for folder_name, xs, ys, num_in_label in data:
            plot_args = self.create_individual_plot_args(folder_name, style_cycle, xs, ys, num_in_label)
            ax.plot(*plot_args["args"], **plot_args["kwargs"])

        # draw limit line:
        if self.cfg.atr["limit"] is not None:
            plt.axhline(y=self.cfg.atr["limit"], color='blue', linestyle='-')

        # draw indicator lines:
        if self.cfg.atr["lines"] and "indicator_lines" in self.cfg.atr.keys():
            utils.plot_lines(self.cfg.atr["indicator_lines"], ax)

        # draw indicator line segments
        if self.cfg.atr["line_segments"] and "indicator_line_segments" in self.cfg.atr.keys() and self.cfg.atr["indicator_line_segments"] is not None:
            utils.plot_line_segments(self.cfg.atr["indicator_line_segments"], ax)

        # create legend:
        legend_kwargs = utils.create_legend_args(self.cfg)
        if legend_kwargs is not []:
            ax.legend(**legend_kwargs)

        # handle axis scale and bounds
        self.handle_axis(ax)

        # draw grid:
        if self.cfg.atr["grid"] and "grid_kwargs" in self.cfg.atr.keys() and self.cfg.atr["grid_kwargs"] is not None:
            ax.grid(**self.cfg.atr["grid_kwargs"])

        # title:
        if self.cfg.atr["title"] is not None:
            plt.title(self.cfg.atr["title"])

        plt.tight_layout()

        # save plot
        plt.savefig(self.cfg.atr["output"])
