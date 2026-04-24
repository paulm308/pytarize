import pandas as pd


def pre_transform_data(data: list[pd.DataFrame], cfg) -> list[pd.DataFrame]:
    transformed = []
    for df in data:
        transformed += [df[df["result"].isin([10, 20])]]
    return transformed
