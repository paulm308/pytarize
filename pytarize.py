from src import parse_zummary
import argparse
import pandas
from pathlib import Path


if __name__ == "__main__":
    parser = argparse.ArgumentParser("TODO")

    parser.add_argument('zummarize', help='Path to the zummarize tool.')
    parser.add_argument('log_path', help='Path to the directory containing the log-files.')

    args = parser.parse_args()

    zummarize_path = Path(args.zummarize)
    log_path = Path(args.log_path)

    df = parse_zummary.parse_zummary(log_path, zummarize_path)
    print(df.loc[0:5])
