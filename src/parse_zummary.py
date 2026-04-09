from pathlib import Path
import pandas as pd
import subprocess
import os
import sys


def parse_zummary(log_path: Path, zummarize_path: Path):
    # convert rellative paths to absolute paths
    log_path = log_path.resolve()
    zummarize_path = zummarize_path.resolve()

    if not log_path.exists():
        raise FileNotFoundError("Path to logfile directory does not exist")
    if not log_path.is_dir():
        raise NotADirectoryError("Path does not lead to a directory")
    if not (any(log_path.glob("*.log")) or any(log_path.glob("*.err"))):
        raise ValueError("Directory does not contain a .log or .err file")

    zummary_path: Path = log_path / "zummary"

    if not zummary_path.exists():
        if not zummarize_path.exists():
            raise FileNotFoundError("Path to zummarize does not exist")
        if not os.access(zummarize_path, os.X_OK):
            print(f"Error: '{zummarize_path}' is not executable.")
            sys.exit(1)

        try:
            result = subprocess.run([zummarize_path, log_path])
            print(result)
        except subprocess.CalledProcessError as e:
            print("The program exited with an error:")
            print(e.stderr)
        except Exception as e:
            print(f"Unexpected error: {e}")

    df: pd.DataFrame = pd.read_csv(zummary_path, delimiter=' ')
    return df
