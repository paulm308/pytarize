from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from src.core.configuration_data import CFG
import pandas as pd

T = TypeVar("T")


class BasePlot(ABC, Generic[T]):
    """
    Abstract parent class for all plot classes.
    """
    cfg: CFG

    def __init__(self, cfg: CFG):
        self.cfg = cfg

    @abstractmethod
    def transform_data(self, data: dict[str, pd.DataFrame]) -> T:
        """
        This function is responsible for all specific calculations and data transformations that are needed to
        create the final plot for the given type.

        Parameters:
        data (dict[str, pd.DataFrame]): A dictionary of all zummarys that are loaded in pandas DataFrames.
        The key of the dictionary is the name of the folder that contains the zummary.

        Returns:
        T: The transformed data that will be used in create_plot to create the final plot.
        """
        pass

    @abstractmethod
    def create_plot(self, data: T):
        """
        This function is responsible for creating and styling the plot.

        Parameters:
        data (T): the output of transform_data.
        """
        pass

    def run(self, data: dict[str, pd.DataFrame]):
        """
        Main function of each plot type. Creates the plot from loaded zummarys.

        Parameters:
        data (dict[str, pd.DataFrame]): A dictionary of all zummarys that are loaded in pandas DataFrames.
        The key of the dictionary is the name of the folder that contains the zummary.
        """
        transformed_data = self.transform_data(data)
        self.create_plot(transformed_data)
