import pandas as pd
from src.core.configuration_data import PlotType


def transform(data: dict[str, pd.DataFrame], cfg):
    """
    Performs transformations that are relevant for all plot types. This includes
    --sat, --unsat and --time.

    Paramters:
    data (dict[str, pd.DataFrame]): A dictionary of all zummarys that are loaded in pandas DataFrames.
    The key of the dictionary is the name of the folder that contains the zummary.
    cfg: The configuration.

    Returns:
    dict[str, pd.DataFrame]: The transformed data.
    """
    # handle sat and unsat
    if "--sat" in cfg.zummarize_cli and "--usat" in cfg.zummarize_cli:
        print("error: '--sat-only' and '--unsat-only'")
        return
    elif cfg.plot_type != PlotType.CombinedPlot:
        if "--sat" in cfg.zummarize_cli:
            for folder_name in data.keys():
                data[folder_name] = data[folder_name][data[folder_name]["result"] == 10]
        elif "--unsat" in cfg.zummarize_cli:
            for folder_name in data.keys():
                data[folder_name] = data[folder_name][data[folder_name]["result"] == 20]

    # handle time and real
    if "time" in cfg.global_atr.keys() and cfg.global_atr["time"] and "real" in cfg.global_atr.keys() and cfg.global_atr["real"]:
        print("error: '--real-only' and '--time-only'")
        return
    elif "time" in cfg.global_atr.keys() and cfg.global_atr["time"]:
        for folder_name in data.keys():
            data[folder_name].drop(columns=["real", "rlim"], inplace=True)
    # real is default:
    else:
        for folder_name in data.keys():
            data[folder_name].drop(columns=["time", "tlim"], inplace=True)
            data[folder_name].rename(columns={"real": "time", "rlim": "tlim"}, inplace=True)
