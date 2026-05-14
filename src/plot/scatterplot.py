from src.plot.baseplot import BasePlot
from src.core.configuration_data import CFG
import src.plot.plot_utils as utils
import pandas as pd
from matplotlib import pyplot as plt
from itertools import cycle


class ScatterPlot(BasePlot):
    ninstances: dict[str, int] = {}

    def transform_data(self, data: dict[str, pd.DataFrame]) -> tuple[list[str], dict[str, pd.DataFrame]]:
        # order folder names
        folder_names = []
        if self.cfg.log_paths is not None:
            folder_names = [path.name for path in self.cfg.log_paths]

        # remove unnessecary columns and set realtime to the time limit if the benchmark was not solved
        for folder_name in folder_names:
            data[folder_name].loc[data[folder_name]["result"] == 2, "real"] = data[folder_name]["rlim"]
            data[folder_name].drop(columns=["time", "space", "tlim", "slim"])

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

    def create_individual_plot_args(self, label: str, style_cycle, values: pd.DataFrame):
        kwargs = {}

        style = next(style_cycle)
        kwargs["color"] = style["color"]
        kwargs["marker"] = style["marker"]
        kwargs["label"] = label.upper()

        if "sat_style" in self.cfg.atr.keys() and label in self.cfg.atr["sat_style"].keys():
            if "color" in self.cfg.atr["sat_style"][label].keys():
                kwargs["color"] = self.cfg.atr["sat_style"][label]["color"]
            if "marker" in self.cfg.atr["sat_style"][label].keys():
                kwargs["marker"] = self.cfg.atr["sat_style"][label]["marker"]
            if "label" in self.cfg.atr["sat_style"][label].keys():
                kwargs["label"] = self.cfg.atr["sat_style"][label]["label"]

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
            legend_kwargs["bbox_to_anchor"] = (xlegend, ylegend)
        legend_kwargs["reverse"] = True
        return legend_kwargs

    def handle_axis_special(self, folder_names: list[str], ax):
        xlabel: None | str = None
        ylabel: None | str = None
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

    def create_plot(self, data: tuple[list[str], dict[str, pd.DataFrame]]):

        # handle latex text rendering
        utils.handle_latex(self.cfg)

        fig, ax = plt.subplots()

        style_cycle = cycle(utils.create_style_cycle(self.cfg))

        for label in ["sat", "unsat", "unsolved"]:
            plot_args = self.create_individual_plot_args(label, style_cycle, data[1][label])
            ax.scatter(*plot_args["args"], **plot_args["kwargs"])

        # create legend:
        legend_kwargs = self.create_legend_args()
        ax.legend(**legend_kwargs)

        # handle axis scale and bounds
        utils.handle_axis_basic(self.cfg, ax)
        utils.handle_axis_advanced(self.cfg, ax)
        self.handle_axis_special(data[0], ax)

        # title:
        if self.cfg.atr["title"] is not None:
            plt.title(self.cfg.atr["title"])

        plt.tight_layout()

        # save plot
        plt.savefig(self.cfg.atr["output"])
