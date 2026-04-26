import pandas as pd


def pre_transform_data(data: dict[str, pd.DataFrame], cfg) -> dict[str, pd.DataFrame]:
    for folder_name in data.keys():
        data[folder_name] = data[folder_name][data[folder_name]["result"].isin([10, 20])]
    return data
