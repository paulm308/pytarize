from src.core.normalize import normalize
import src.core.validate as val
from src.core.load_data import read_zummary
from dataclasses import dataclass
import pandas as pd


def run_pipeline(cfg):
    ncfg = normalize(cfg)
    val.validate_log_path(ncfg)
    if not val.check_if_zummary_exists(ncfg):
        val.validate_zummarize_path(ncfg)
    df: pd.DataFrame = read_zummary(cfg)
    print(df.loc[0:5])
