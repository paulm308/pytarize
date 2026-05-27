from src.plot.baseplot import BasePlot
from src.core.configuration_data import CFG
import src.plot.plot_utils as utils
import pandas as pd
from matplotlib import pyplot as plt
from itertools import cycle
from typing import Optional
from matplotlib.markers import MarkerStyle


class CombinedPlot(BasePlot):
    def transform_data(self, data: dict[str, pd.DataFrame]):
        pass

    def create_plot(self, data: tuple[list[str], dict[str, pd.DataFrame]]):
        pass
