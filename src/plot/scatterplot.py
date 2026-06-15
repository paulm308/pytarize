from src.plot.baseplot import BasePlot
from src.core.configuration_data import CFG
import src.plot.plot_utils as utils
import pandas as pd
from matplotlib import pyplot as plt
from itertools import cycle
from typing import Optional
from matplotlib.markers import MarkerStyle
from math import sqrt


class ScatterPlot(BasePlot):
    ninstances: dict[str, int] = {}
    limits: tuple[Optional[float], Optional[float]] = (None, None)
    timeouts: tuple[Optional[float], Optional[float]] = (None, None)
    max_achsvalues: tuple[Optional[float], Optional[float]] = (None, None)

    def transform_data(self, data: dict[str, pd.DataFrame]) -> tuple[list[str], dict[str, pd.DataFrame]]:
        # order folder names
        folder_names = []
        if self.cfg.log_paths is not None:
            folder_names = [path.name for path in self.cfg.log_paths]

        # save limits for "limit" option
        if self.cfg.atr["limit"] or self.cfg.atr["extend"] is not None:
            self.limits = (data[folder_names[0]]["rlim"][0], data[folder_names[1]]["rlim"][0])

        self.timeouts = self.compute_timeouts_and_max_achsvalues((data[folder_names[0]]["rlim"][0], data[folder_names[1]]["rlim"][0]))

        # remove unnessecary columns and set realtime to the time limit if the benchmark was not solved
        for idx, folder_name in enumerate(folder_names):
            data[folder_name].loc[data[folder_name]["result"] < 10, "real"] = self.timeouts[idx]
            data[folder_name].drop(columns=["time", "space", "tlim", "slim"], inplace=True)

        # merge zummarys by benchmark name
        merged = pd.merge(data[folder_names[0]], data[folder_names[1]], on='Unnamed: 0', how="inner")

        # calculate number of sat, unsat and unsolved instances
        if self.cfg.atr["show_solved"]:
            combined = pd.concat([data[folder_names[0]], data[folder_names[1]]], ignore_index=True)
            self.ninstances["sat"] = combined.loc[combined.iloc[:, 1] == 10, combined.columns[0]].nunique()
            self.ninstances["unsat"] = combined.loc[combined.iloc[:, 1] == 20, combined.columns[0]].nunique()
            self.ninstances["unsolved"] = combined.loc[combined.iloc[:, 1] < 10, combined.columns[0]].nunique()

        # split table is satisfiable, unsatisfiable and unsolved tables
        sat = merged[(merged["result_x"] == 10) | (merged["result_y"] == 10)]
        unsat = merged[(merged["result_x"] == 20) | (merged["result_y"] == 20)]
        unsolved = merged[(merged["result_x"].isin([1, 2])) & (merged["result_y"].isin([1, 2]))]

        res = {
            "sat": sat,
            "unsat": unsat,
            "unsolved": unsolved
        }

        return (folder_names, res)

    def compute_timeouts_and_max_achsvalues(self, limits: tuple[float, float]) -> tuple[float, float]:
        if self.cfg.atr["extend"] is not None:
            xmin = self.cfg.atr["xmin"]
            xmax = limits[0]
            ymin = self.cfg.atr["ymin"]
            ymax = limits[1]

            if (xmin is not None and xmax is not None and ymin is not None and ymax is not None):
                f = self.cfg.atr["extend"]
                xmax_new = xmin + (xmax - xmin) / f
                ymax_new = ymin + (ymax - ymin) / f
                xtimeout = (xmax_new - limits[0]) / 2 + limits[0]
                ytimeout = (ymax_new - limits[1]) / 2 + limits[1]
                if self.cfg.atr["xlog"]:
                    xmax_new = xmin * (xmax / xmin) ** (1 / f)
                    xtimeout = sqrt(limits[0] * xmax_new)
                if self.cfg.atr["ylog"]:
                    ymax_new = ymin * (ymax / ymin) ** (1 / f)
                    ytimeout = sqrt(limits[1] * ymax_new)
                self.max_achsvalues = (xmax_new, ymax_new)
                return (xtimeout, ytimeout)
            else:
                print(f"extend requires that xmin, xmax, ymin and ymax have been set. xmin: {xmin}, xmax: {xmax}, ymin: {ymin}, ymax: {ymax}")
        self.max_achsvalues = (self.cfg.atr["xmax"], self.cfg.atr["xmax"])
        return limits

    def create_individual_plot_args(self, label: str, style_cycle, values: pd.DataFrame):
        kwargs = {}

        style = next(style_cycle)
        color = style["color"]
        kwargs["marker"] = style["marker"]
        kwargs["label"] = label.upper()

        if kwargs["marker"] not in MarkerStyle.filled_markers:
            kwargs["facecolors"] = style["color"]

        if "sat_style" in self.cfg.atr.keys() and label in self.cfg.atr["sat_style"].keys():
            if "color" in self.cfg.atr["sat_style"][label].keys():
                color = self.cfg.atr["sat_style"][label]["color"]
            if "marker" in self.cfg.atr["sat_style"][label].keys():
                kwargs["marker"] = self.cfg.atr["sat_style"][label]["marker"]
            if "label" in self.cfg.atr["sat_style"][label].keys():
                kwargs["label"] = self.cfg.atr["sat_style"][label]["label"]
            kwargs.update(self.cfg.atr["sat_style"][label])

        # create holow markers
        if kwargs["marker"] in MarkerStyle.filled_markers and self.cfg.atr["hollow"]:
            kwargs["markeredgecolor"] = color
            kwargs["markerfacecolor"] = "none"
        kwargs["color"] = color

        if self.cfg.atr["show_solved"]:
            kwargs["label"] = f"{self.ninstances[label]} {kwargs['label']}"

        xs = values["real_x"]
        ys = values["real_y"]
        args = (xs, ys)

        return {"args": args, "kwargs": kwargs}

    def create_legend_args(self):
        legend_kwargs = {}
        if self.cfg.atr["center"]:
            legend_kwargs["loc"] = "center right"
        if self.cfg.atr["xlegend"] is not None or self.cfg.atr["ylegend"] is not None:
            xlegend = 0.5 if self.cfg.atr["xlegend"] is None else self.cfg.atr["xlegend"]
            ylegend = 0.5 if self.cfg.atr["ylegend"] is None else self.cfg.atr["ylegend"]
            legend_kwargs["loc"] = "center"
            legend_kwargs["bbox_to_anchor"] = (xlegend, ylegend)
        legend_kwargs["reverse"] = True
        return legend_kwargs

    def handle_axis(self, folder_names: list[str], ax):
        utils.handle_axis_basic(self.cfg, ax)
        if self.cfg.atr["extend"] is not None:
            utils.disable_ticks_after_threshold(ax, self.limits)  # type: ignore
            utils.append_major_tick(self.timeouts, ax)  # type: ignore
        ax.set_xlim(self.cfg.atr["xmin"], self.max_achsvalues[0])
        ax.set_ylim(self.cfg.atr["ymin"], self.max_achsvalues[1])
        if self.cfg.atr["square_box"]:
            utils.change_boundingbox_shape_to_square(ax)

        xlabel: Optional[str] = None
        ylabel: Optional[str] = None
        if "solver_style" in self.cfg.atr.keys():
            if folder_names[0] in self.cfg.atr["solver_style"].keys() and "label" in self.cfg.atr["solver_style"][folder_names[0]].keys():
                xlabel = self.cfg.atr["solver_style"][folder_names[0]]["label"]
            if folder_names[1] in self.cfg.atr["solver_style"].keys() and "label" in self.cfg.atr["solver_style"][folder_names[1]].keys():
                ylabel = self.cfg.atr["solver_style"][folder_names[1]]["label"]
        if self.cfg.atr["xlabel"] is not None:
            xlabel = self.cfg.atr["xlabel"]
        if self.cfg.atr["ylabel"] is not None:
            ylabel = self.cfg.atr["ylabel"]
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if self.cfg.atr["plain"]:
            utils.change_tick_notation_label(ax, self.timeouts, "TO", self.cfg)  # type: ignore

    def create_plot(self, data: tuple[list[str], dict[str, pd.DataFrame]]):

        # handle latex text rendering
        utils.handle_latex(self.cfg)

        subplots_kwargs = {}
        if "subplots_kwargs" in self.cfg.atr.keys():
            subplots_kwargs = self.cfg.atr["subplots_kwargs"]

        fig, ax = plt.subplots(**subplots_kwargs)

        style_cycle = cycle(utils.create_style_cycle(self.cfg))

        for label in ["sat", "unsat", "unsolved"]:
            plot_args = self.create_individual_plot_args(label, style_cycle, data[1][label])
            ax.scatter(*plot_args["args"], **plot_args["kwargs"])

        # create limit lines:
        if self.cfg.atr["limit"]:
            ax.plot([0, self.limits[0], self.limits[0]], [self.limits[1], self.limits[1], 0], color="black", linestyle="--", zorder=0)  # type:ignore

        # plot extended timout line
        if self.cfg.atr["extend"]:
            ax.plot([0, self.timeouts[0], self.timeouts[0]], [self.timeouts[1], self.timeouts[1], 0], color="red", zorder=0)  # type:ignore

        # create legend:
        legend_kwargs = self.create_legend_args()
        ax.legend(**legend_kwargs)

        # handle axis scale and bounds labels, ticks
        self.handle_axis(data[0], ax)

        # draw indicator lines:
        if self.cfg.atr["lines"] and "indicator_lines" in self.cfg.atr.keys() and self.cfg.atr["indicator_lines"] is not None:
            utils.plot_lines(self.cfg.atr["indicator_lines"], ax)

        # draw indicator line segments
        if self.cfg.atr["line_segments"] and "indicator_line_segments" in self.cfg.atr.keys() and self.cfg.atr["indicator_line_segments"] is not None:
            utils.plot_line_segments(self.cfg.atr["indicator_line_segments"], ax)

        # draw grid:
        if self.cfg.atr["grid"] and "grid_kwargs" in self.cfg.atr.keys() and self.cfg.atr["grid_kwargs"] is not None:
            ax.grid(**self.cfg.atr["grid_kwargs"])

        # title:
        if self.cfg.atr["title"] is not None:
            plt.title(self.cfg.atr["title"])

        plt.tight_layout()

        # save plot
        plt.savefig(self.cfg.atr["output"])
