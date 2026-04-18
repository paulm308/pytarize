from src.core.validate import validate_zummarize_path
from src.core.handle_zummarize import call_zummarize


def enshure_zummary(cfg):
    paths_without_zummary = []
    for log_path in cfg.log_paths:
        if (log_path / "zummary").exists():
            continue
        paths_without_zummary.append(log_path)
    if paths_without_zummary != []:
        validate_zummarize_path(cfg.zummarize_path)
        call_zummarize(cfg)
