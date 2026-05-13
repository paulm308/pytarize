from src.plot.baseplot import BasePlot
from src.core.configuration_data import CFG
import src.plot.plot_utils as utils
import pandas as pd
from matplotlib import pyplot as plt
from itertools import cycle


class ScatterPlot(BasePlot):
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

        # split table is satisfiable, unsatisfiable and unsolved tables
        sat = merged[(merged["result_x"] == 10) | (merged["result_y"] == 10)]
        unsat = merged[(merged["result_x"] == 20) | (merged["result_y"] == 20)]
        unsolved = merged[(merged["result_x"].isin([1, 2])) & (merged["result_y"].isin([1, 2]))]

        res = {
            "sat": sat,
            "unsat": unsat,
            "unsolved": unsolved
        }

        # print(f"original: {data[folder_name].shape[0]}, merged: {merged.shape[0]}, sat: {sat.shape[0]}, unsat: {unsat.shape[0]}, unsolved: {unsolved.shape[0]}")
        # print(merged.iloc[:5])
        return (folder_names, res)

    def create_individual_plot_args(self, label: str, style_cycle, values: pd.DataFrame, cfg: CFG):
        kwargs = {}

        style = next(style_cycle)
        color = style["color"]
        marker = style["marker"]

        if "sat_style" in cfg.atr.keys() and label in cfg.atr["sat_style"].keys():
            if "color" in cfg.atr["sat_style"][label].keys():
                color = cfg.atr["sat_style"][label]["color"]
            if "marker" in cfg.atr["sat_style"][label].keys():
                marker = cfg.atr["sat_style"][label]["marker"]

        kwargs["color"] = color
        kwargs["marker"] = marker

        xs = values["real_x"]
        ys = values["real_y"]
        args = (xs, ys)

        return {"args": args, "kwargs": kwargs}

    def create_plot(self, data: tuple[list[str], dict[str, pd.DataFrame]], cfg: CFG):

        # handle latex text rendering
        utils.handle_latex(cfg)

        fig, ax = plt.subplots()

        style_cycle = iter(utils.create_style_cycle(cfg))

        for label in ["sat", "unsat", "unsolved"]:
            plot_args = self.create_individual_plot_args(label, style_cycle, data[1][label], cfg)
            ax.scatter(*plot_args["args"], **plot_args["kwargs"])

        # handle axis scale and bounds
        utils.handle_axis(cfg)

        # title:
        if cfg.atr["title"] is not None:
            plt.title(cfg.atr["title"])

        plt.tight_layout()

        # save plot
        plt.savefig(cfg.atr["output"])
