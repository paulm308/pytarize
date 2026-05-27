from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from src.core.configuration_data import CFG
import pandas as pd

T = TypeVar("T")


class BasePlot(ABC, Generic[T]):
    cfg: CFG

    def __init__(self, cfg: CFG):
        self.cfg = cfg

    @abstractmethod
    def transform_data(self, data: dict[str, pd.DataFrame]) -> T:
        pass

    @abstractmethod
    def create_plot(self, data: T):
        pass

    def run(self, data: dict[str, pd.DataFrame]):
        transformed_data = self.transform_data(data)
        self.create_plot(transformed_data)
