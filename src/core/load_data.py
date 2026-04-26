import pandas as pd


def read_zummary(cfg) -> dict[str, pd.DataFrame]:
    res = {}
    for log_path in cfg.log_paths:
        zummary_path = log_path / "zummary"
        df = pd.read_csv(zummary_path, delimiter=' ')
        folder_name = log_path.name
        res[folder_name] = df
    return res
