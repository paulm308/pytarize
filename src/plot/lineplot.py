from src.plot.baseplot import BasePlot
from src.core.configuration_data import CFG
import pandas as pd
import numpy as np
from typing import Generic, TypeVar
from matplotlib import pyplot as plt


class LinePlot(BasePlot):

    def transform_data(self, data: list[pd.DataFrame], cfg: CFG) -> list[list[float]]:
        transformed = []
        for df in data:
            transformed.append(np.sort(df["time"].to_numpy()))
        return transformed

    def create_plot(self, data: list[list[float]], cfg: CFG):
        fig, ax = plt.subplots()

        for ys in data:
            ax.plot(range(1, len(ys) + 1), ys)

        plt.tight_layout()
        plt.savefig("plot.png")
