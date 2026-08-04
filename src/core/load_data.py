import pandas as pd


def read_zummary(cfg) -> dict[str, pd.DataFrame]:
    """
    Loads all zummarys in pandas dataframes.

    Parameters:
    cfg: The configuration.

    Returns:
    dict[str, pd.DataFrame]: A dictionary of all zummarys that are loaded in pandas DataFrames.
    The key of the dictionary is the name of the folder that contains the zummary.
    """
    res = {}
    for log_path in cfg.log_paths:
        zummary_path = log_path / "zummary"
        df = pd.read_csv(zummary_path, delimiter=' ')
        folder_name = log_path.name
        res[folder_name] = df
    return res
