from src.core.normalize import normalize, normalize_r_log_paths
from src.core.validate import validate_log_paths, pre_validate_log_paths, validate_zummarize_path
from src.core.load_data import read_zummary
from src.core.handle_recursive_log_paths import extract_log_paths
from src.core.handle_zummarize import call_zummarize, zummarize_required
from src.core.initialize_plot import run_plots
from src.core.save_data import save_config
from src.core.transform import transform


def run_pipeline(cfg):
    pre_validate_log_paths(cfg)
    normalize_r_log_paths(cfg)
    extract_log_paths(cfg)
    normalize(cfg)
    validate_log_paths(cfg)
    validate_zummarize_path(cfg)
    if zummarize_required(cfg):
        call_zummarize(cfg)
    save_config(cfg)
    data = read_zummary(cfg)
    transform(data, cfg)
    run_plots(data, cfg)
