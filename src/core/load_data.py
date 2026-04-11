import pandas as pd


def read_zummary(cfg) -> pd.DataFrame:
    return pd.read_csv((cfg.log_path / "zummary"), delimiter=' ')
