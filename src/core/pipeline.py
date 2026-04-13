from src.core.normalize import normalize
from src.core.validate import validate_log_paths
from src.core.load_data import read_zummary
from src.core.handle_zummary import enshure_zummary
import pandas as pd


def run_pipeline(cfg):
    ncfg = normalize(cfg)
    validate_log_paths(ncfg)
    enshure_zummary(ncfg)
    data = read_zummary(ncfg)
    print(ncfg)
    for df in data:
        print(df.loc[0:5])
