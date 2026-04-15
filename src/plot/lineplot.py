from src.plot.baseplot import BasePlot
from src.core.configuration_data import CFG
import pandas as pd
from typing import Generic, TypeVar


class LinePlot(BasePlot):

    def transform_data(self, data: list[pd.DataFrame], cfg: CFG) -> list[list[float]]:
        pass  # TODO

    def create_plot(self, data: list[list[float]], cfg: CFG):
        pass  # TODO
