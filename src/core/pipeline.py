from src.core.normalize import normalize, normalize_r_log_paths
from src.core.validate import validate_log_paths, pre_validate_log_paths
from src.core.load_data import read_zummary
from src.core.handle_zummary import enshure_zummary
from src.core.handle_recursive_log_paths import extract_log_paths


def run_pipeline(cfg):
    pre_validate_log_paths(cfg)
    normalize_r_log_paths(cfg)
    extract_log_paths(cfg)
    ncfg = normalize(cfg)
    validate_log_paths(ncfg)
    enshure_zummary(ncfg)
    data = read_zummary(ncfg)
    print(ncfg)
    for df in data:
        print(df.loc[0:5])
