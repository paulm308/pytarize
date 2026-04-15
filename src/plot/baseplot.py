from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from src.core.configuration_data import CFG
import pandas as pd

T = TypeVar("T")


class BasePlot(ABC, Generic[T]):

    @abstractmethod
    def transform_data(self, data: list[pd.DataFrame], cfg: CFG) -> T:
        pass

    @abstractmethod
    def create_plot(self, data: T, cfg: CFG):
        pass

    def run(self, data: list[pd.DataFrame], cfg: CFG):
        transformed_data = self.transform_data(data, cfg)
        self.create_plot(transformed_data, cfg)
