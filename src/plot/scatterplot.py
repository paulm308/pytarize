from src.plot.baseplot import BasePlot
from src.core.configuration_data import CFG
import pandas as pd
from matplotlib import pyplot as plt


class ScatterPlot(BasePlot):
    def transform_data(self, data: dict[str, pd.DataFrame], cfg: CFG) -> tuple[list[str], list[pd.DataFrame]]:
        # order folder names
        folder_names = []
        if cfg.log_paths is not None:
            folder_names = [path.name for path in cfg.log_paths]

        # remove unnessecary comuns and set realtime to the time limit if the benchmark was not solved
        for folder_name in folder_names:
            data[folder_name].loc[data[folder_name]["result"] == 2, "real"] = data[folder_name]["rlim"]
            data[folder_name].drop(columns=["time", "space", "tlim", "slim"])

        # merge zummarys by benchmark name
        merged = pd.merge(data[folder_names[0]], data[folder_names[1]], on='Unnamed: 0', how="inner")

        # split table is satisfiable, unsatisfiable and unsolved tables
        sat = merged[(merged["result_x"] == 10) | (merged["result_y"] == 10)]
        unsat = merged[(merged["result_x"] == 20) | (merged["result_y"] == 20)]
        unsolved = merged[(merged["result_x"].isin([1, 2])) & (merged["result_y"].isin([1, 2]))]

        # print(f"original: {data[folder_name].shape[0]}, merged: {merged.shape[0]}, sat: {sat.shape[0]}, unsat: {unsat.shape[0]}, unsolved: {unsolved.shape[0]}")
        # print(merged.iloc[:5])
        return (folder_names, [sat, unsat, unsolved])

    def create_plot(self, data: tuple[list[str], list[pd.DataFrame]], cfg: CFG):
        # sat:
        plt.scatter(data[1][0]["real_x"], data[1][0]["real_y"], marker="x")

        # unsat:
        plt.scatter(data[1][1]["real_x"], data[1][1]["real_y"], marker="o")

        # unsolved:
        plt.scatter(data[1][2]["real_x"], data[1][2]["real_y"], marker="+")

        plt.xscale("log")
        plt.yscale("log")

        plt.tight_layout()

        plt.savefig("scatter.png")
