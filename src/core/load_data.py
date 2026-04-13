import pandas as pd


def read_zummary(cfg) -> list[pd.DataFrame]:
    res = []
    for log_path in cfg.log_paths:
        zummary_path = log_path / "zummary"
        df = pd.read_csv(zummary_path, delimiter=' ')
        res.append(df)
    return res
