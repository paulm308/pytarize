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
