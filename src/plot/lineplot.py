from src.plot.baseplot import BasePlot
import src.plot.plot_utils as utils
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from itertools import cycle
from matplotlib.markers import MarkerStyle


class LinePlot(BasePlot):

    def transform_data(self, data: dict[str, pd.DataFrame]) -> list[tuple[str, list[float], list[float]]]:

        for folder_name in data.keys():
            data[folder_name] = data[folder_name][data[folder_name]["result"].isin([10, 20])]

        transformed = []
        for folder_name, values in data.items():
            tup = (folder_name, np.sort(values["time"].to_numpy()), list(range(1, len(values) + 1)))
            transformed.append(tup)

        # sort the data so that the best run is first in the list
        transformed = sorted(transformed,
                             key=lambda x: len(x[1]))

        # for tup in reversed(transformed):
        #     print(f"{len(tup[1])}   {tup[0]}")

        if self.cfg.atr["cactus"]:
            transformed = [(tup[0], tup[2], tup[1]) for tup in transformed]

        return transformed

    def create_individual_plot_args(self, folder_name: str, style_cycle, xs: list[float], ys: list[float]):
        kwargs = {}

        style = next(style_cycle)
        color = style["color"]
        kwargs["marker"] = style["marker"]
        kwargs["label"] = folder_name

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
        if kwargs["marker"] in MarkerStyle.filled_markers and self.cfg.atr["hollow"]:
            kwargs["markeredgecolor"] = color
            kwargs["markerfacecolor"] = "none"
        kwargs["color"] = color

        # show solved count in legend:
        if self.cfg.atr["show_solved"]:
            kwargs["label"] = f"{len(ys)} {kwargs['label']}"
        args = (xs, ys)

        return {"args": args, "kwargs": kwargs}

    def create_legend_args(self):
        legend_kwargs = {}
        if "legend_kwargs" in self.cfg.atr.keys():
            legend_kwargs = self.cfg.atr["legend_kwargs"]
        if self.cfg.atr["center"]:
            if self.cfg.atr["cactus"]:
                legend_kwargs["loc"] = "center left"
            else:
                legend_kwargs["loc"] = "center right"
        if self.cfg.atr["xlegend"] is not None or self.cfg.atr["ylegend"] is not None:
            xlegend = 0.5 if self.cfg.atr["xlegend"] is None else self.cfg.atr["xlegend"]
            ylegend = 0.5 if self.cfg.atr["ylegend"] is None else self.cfg.atr["ylegend"]
            legend_kwargs["loc"] = "center"
            legend_kwargs["bbox_to_anchor"] = (xlegend, ylegend)
        legend_kwargs["reverse"] = True
        return legend_kwargs

    def handle_axis(self, ax):
        utils.handle_axis_basic(self.cfg, ax)
        ax.set_xlim(self.cfg.atr["xmin"], self.cfg.atr["xmax"])
        ax.set_ylim(self.cfg.atr["ymin"], self.cfg.atr["ymax"])
        ax.set_xlabel(self.cfg.atr["xlabel"])
        ax.set_ylabel(self.cfg.atr["ylabel"])
        if self.cfg.atr["plain"]:
            utils.change_tick_notation_label(ax, None, None, self.cfg)

    def create_plot(self, data: list[tuple[str, list[float], list[float]]]):

        # handle latex text rendering
        utils.handle_latex(self.cfg)

        subplots_kwargs = {}
        if "subplots_kwargs" in self.cfg.atr.keys():
            subplots_kwargs = self.cfg.atr["subplots_kwargs"]

        fig, ax = plt.subplots(**subplots_kwargs)

        # create style cycle (markers and colors)
        style_cycle = cycle(utils.create_style_cycle(self.cfg))

        for folder_name, xs, ys in data:
            plot_args = self.create_individual_plot_args(folder_name, style_cycle, xs, ys)
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
        legend_kwargs = self.create_legend_args()
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
