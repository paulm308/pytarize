from src.plot.baseplot import BasePlot
from src.core.configuration_data import CFG
import pandas as pd
import numpy as np
from typing import Generic, TypeVar
from matplotlib import pyplot as plt


class LinePlot(BasePlot):

    def transform_data(self, data: dict[str, pd.DataFrame], cfg: CFG) -> list[tuple[str, list[float]]]:
        transformed = []
        for folder_name, values in data.items():
            tup = (folder_name, np.sort(values["time"].to_numpy()))
            transformed.append(tup)

        # sort the data so that the best run is first in the list
        min_length = min([len(x[1]) for x in transformed])
        if min_length != 0:
            transformed = sorted(transformed,
                                 key=lambda x: x[1][min_length - 1])

        return transformed

    def create_plot(self, data: list[tuple[str, list[float]]], cfg: CFG):
        fig, ax = plt.subplots()

        for folder_name, values in data:
            ax.plot(values, range(1, len(values) + 1),
                    label=folder_name)

        ax.legend()
        plt.tight_layout()
        plt.savefig("plot.png")
