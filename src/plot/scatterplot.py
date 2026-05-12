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
    def transform_data(self, data: dict[str, pd.DataFrame], cfg: CFG) -> list[tuple[str, list[float]]]:
        pass

    def create_plot(self, data: list[tuple[str, list[float]]], cfg: CFG):
        pass
