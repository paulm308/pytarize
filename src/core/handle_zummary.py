from src.core.validate import validate_zummarize_path
from src.core.recompute_zummary import generate_zummary


def enshure_zummary(cfg):
    zummize_path_validated = False
    for log_path in cfg.log_paths:
        if (log_path / "zummary").exists():
            continue
        if not zummize_path_validated:
            validate_zummarize_path(cfg.zummarize_path)
        generate_zummary(cfg.zummarize_path, log_path)
