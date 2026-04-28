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

        fig, ax = plt.subplots()

        # line styles:
        # create marker and color cycle:
        n = lcm(len(cfg.atr["colors"]), len(cfg.atr["markers"]))
        color_cycle = utils.initialize_color(cfg.atr["colors"])
        combined = cycler(
            color=list(islice(cycle(color_cycle), n)),
            marker=list(islice(cycle(cfg.atr["markers"]), n)),
        )
        ax.set_prop_cycle(combined)

        # show solved count in legend:
        if cfg.atr["show_solved"]:
            data = utils.add_solved_to_folder_name(data)

        # plot data:
        for folder_name, values in data:
            xs = values
            ys = range(1, len(values) + 1)
            if cfg.atr["cactus"]:
                xs = range(1, len(values) + 1)
                ys = values
            ax.plot(xs, ys, label=folder_name)

        # create legend:
        legend_orientation = 0
        if cfg.atr["center"]:
            if cfg.atr["cactus"]:
                legend_orientation = 6
            else:
                legend_orientation = 7
        ax.legend(loc=legend_orientation)

        plt.tight_layout()
        plt.savefig("plot.png")
