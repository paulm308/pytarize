from src.plot.baseplot import BasePlot
from src.core.configuration_data import CFG
import src.plot.plot_utils as utils
import pandas as pd
import numpy as np
from typing import Generic, TypeVar
from matplotlib import pyplot as plt
from cycler import cycler


class LinePlot(BasePlot):

    def transform_data(self, data: dict[str, pd.DataFrame], cfg: CFG) -> list[tuple[str, list[float]]]:
        transformed = []
        for folder_name, values in data.items():
            tup = (folder_name, np.sort(values["time"].to_numpy()))
            transformed.append(tup)

        # sort the data so that the best run is first in the list
        transformed = sorted(transformed,
                             key=lambda x: x[1][len(x[1]) - 1])

        return transformed

    def create_plot(self, data: list[tuple[str, list[float]]], cfg: CFG):

        # line color:
        color_cycle = cycler(color=utils.initialize_color(cfg.atr["color"]))
        plt.rcParams["axes.prop_cycle"] = color_cycle

        fig, ax = plt.subplots()

        for folder_name, values in data:
            ax.plot(values, range(1, len(values) + 1),
                    label=folder_name)

        ax.legend()
        plt.tight_layout()
        plt.savefig("plot.png")
