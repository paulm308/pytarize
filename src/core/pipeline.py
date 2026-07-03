import src.core.handle_paths as pts
from src.core.load_data import read_zummary
from src.core.handle_zummarize import call_zummarize, zummarize_required
from src.core.initialize_plot import run_plots
from src.core.save_data import save_config
from src.core.transform import transform


def run_pipeline(cfg):
    pts.pre_validate_log_paths(cfg)
    pts.normalize_r_log_paths(cfg)
    pts.extract_log_paths(cfg)
    pts.normalize(cfg)
    pts.validate_log_paths(cfg)
    pts.validate_zummarize_path(cfg)
    if zummarize_required(cfg):
        call_zummarize(cfg)
    save_config(cfg)
    data = read_zummary(cfg)
    transform(data, cfg)
    run_plots(data, cfg)
