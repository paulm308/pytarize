import pandas as pd


def transform(data: dict[str, pd.DataFrame], cfg):
    if "--sat" in cfg.zummarize_cli and "--usat" in cfg.zummarize_cli:
        print("error: '--sat-only' and '--unsat-only'")
        return
    elif "--sat" in cfg.zummarize_cli:
        for folder_name in data.keys():
            data[folder_name] = data[folder_name][data[folder_name]["result"] == 10]
    elif "--unsat" in cfg.zummarize_cli:
        for folder_name in data.keys():
            data[folder_name] = data[folder_name][data[folder_name]["result"] == 20]

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
