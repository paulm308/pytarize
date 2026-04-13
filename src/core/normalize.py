
def normalize(cfg):
    # convert rellative paths to absolute paths
    if cfg.zummarize_path is not None:
        cfg.zummarize_path = cfg.zummarize_path.expanduser().resolve()
    paths = []
    for log_path in cfg.log_paths:
        paths.append(log_path.expanduser().resolve())
    cfg.log_paths = paths
    cfg.base_config_path = cfg.base_config_path.expanduser().resolve()
    cfg.plot_config_path = cfg.base_config_path.expanduser().resolve()
    return cfg
