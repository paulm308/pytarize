from src.plot.baseplot import BasePlot
from src.core.configuration_data import CFG
import src.plot.plot_utils as utils
import pandas as pd
from matplotlib import pyplot as plt
from itertools import cycle


class ScatterPlot(BasePlot):
    ninstances: dict[str, int] = {}

    def transform_data(self, data: dict[str, pd.DataFrame], cfg: CFG) -> tuple[list[str], dict[str, pd.DataFrame]]:
        # order folder names
        folder_names = []
        if cfg.log_paths is not None:
            folder_names = [path.name for path in cfg.log_paths]

        # remove unnessecary columns and set realtime to the time limit if the benchmark was not solved
        for folder_name in folder_names:
            data[folder_name].loc[data[folder_name]["result"] == 2, "real"] = data[folder_name]["rlim"]
            data[folder_name].drop(columns=["time", "space", "tlim", "slim"])

        # merge zummarys by benchmark name
        merged = pd.merge(data[folder_names[0]], data[folder_names[1]], on='Unnamed: 0', how="inner")

        # calculate number of sat, unsat and unsolved instances
        if cfg.atr["show_solved"]:
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

    def create_individual_plot_args(self, label: str, style_cycle, values: pd.DataFrame, cfg: CFG):
        kwargs = {}

        style = next(style_cycle)
        kwargs["color"] = style["color"]
        kwargs["marker"] = style["marker"]
        kwargs["label"] = label.upper()

        if "sat_style" in cfg.atr.keys() and label in cfg.atr["sat_style"].keys():
            if "color" in cfg.atr["sat_style"][label].keys():
                kwargs["color"] = cfg.atr["sat_style"][label]["color"]
            if "marker" in cfg.atr["sat_style"][label].keys():
                kwargs["marker"] = cfg.atr["sat_style"][label]["marker"]
            if "label" in cfg.atr["sat_style"][label].keys():
                kwargs["label"] = cfg.atr["sat_style"][label]["label"]

        if cfg.atr["show_solved"]:
            kwargs["label"] = f"{self.ninstances[label]} {kwargs['label']}"

        xs = values["real_x"]
        ys = values["real_y"]
        args = (xs, ys)

        return {"args": args, "kwargs": kwargs}

    def create_legend_args(self, cfg: CFG):
        legend_kwargs = {}
        if cfg.atr["center"]:
            legend_kwargs["loc"] = "center right"
        if cfg.atr["xlegend"] is not None or cfg.atr["ylegend"] is not None:
            xlegend = 0.5 if cfg.atr["xlegend"] is None else cfg.atr["xlegend"]
            ylegend = 0.5 if cfg.atr["ylegend"] is None else cfg.atr["ylegend"]
            legend_kwargs["bbox_to_anchor"] = (xlegend, ylegend)
        legend_kwargs["reverse"] = True
        return legend_kwargs

    def create_plot(self, data: tuple[list[str], dict[str, pd.DataFrame]], cfg: CFG):

        # handle latex text rendering
        utils.handle_latex(cfg)

        fig, ax = plt.subplots()

        style_cycle = iter(utils.create_style_cycle(cfg))

        for label in ["sat", "unsat", "unsolved"]:
            plot_args = self.create_individual_plot_args(label, style_cycle, data[1][label], cfg)
            ax.scatter(*plot_args["args"], **plot_args["kwargs"])

        # create legend:
        legend_kwargs = self.create_legend_args(cfg)
        ax.legend(**legend_kwargs)

        # handle axis scale and bounds
        utils.handle_axis(cfg)

        # title:
        if cfg.atr["title"] is not None:
            plt.title(cfg.atr["title"])

        plt.tight_layout()

        # save plot
        plt.savefig(cfg.atr["output"])
