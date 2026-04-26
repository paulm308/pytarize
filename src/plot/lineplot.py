from src.plot.baseplot import BasePlot
from src.core.configuration_data import CFG
import pandas as pd
import numpy as np
from typing import Generic, TypeVar
from matplotlib import pyplot as plt


class LinePlot(BasePlot):

    def transform_data(self, data: dict[str, pd.DataFrame], cfg: CFG) -> dict[str, list[float]]:
        transformed = {}
        for folder_name in data.keys():
            transformed[folder_name] = np.sort(data[folder_name]["time"].to_numpy())
        return transformed

    def create_plot(self, data: dict[str, list[float]], cfg: CFG):
        fig, ax = plt.subplots()

        for folder_name in data.keys():
            ax.plot(data[folder_name], range(1, len(data[folder_name]) + 1),
                    label=folder_name)

        ax.legend()
        plt.tight_layout()
        plt.savefig("plot.png")
