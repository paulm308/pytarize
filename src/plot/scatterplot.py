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


class ScatterPlot(BasePlot):
    def transform_data(self, data: dict[str, pd.DataFrame], cfg: CFG) -> tuple[list[str], pd.DataFrame]:
        folder_names = list(data.keys())
        for folder_name in folder_names:
            data[folder_name].loc[data[folder_name]["result"] == 2, "real"] = data[folder_name]["rlim"]
            data[folder_name].drop(columns=["time", "space", "tlim", "slim"])
        merged = pd.merge(data[folder_names[0]], data[folder_names[1]], on='Unnamed: 0', how="inner")
        print(merged.iloc[:5])
        return (folder_names, merged)

    def create_plot(self, data: tuple[list[str], pd.DataFrame], cfg: CFG):
        plt.scatter(data[1]["real_x"], data[1]["real_y"], marker="x")
        plt.savefig("scatter.png")
