from src.plot.baseplot import BasePlot
from src.core.configuration_data import CFG
import pandas as pd
from typing import Generic, TypeVar
from matplotlib import pyplot as plt


class LinePlot(BasePlot):

    def transform_data(self, data: list[pd.DataFrame], cfg: CFG) -> list[list[float]]:
        pass  # TODO

    def create_plot(self, data: list[list[float]], cfg: CFG):
        fig, ax = plt.subplots()

        # data[0] should be the x axis
        for ys in data[1:]:
            ax.plot(data[0], ys)

        plt.tight_layout()
        plt.show()
