
def normalize(cfg):
    # convert rellative paths to absolute paths
    if cfg.zummarize_path is not None:
        cfg.zummarize_path = cfg.zummarize_path.expanduser().resolve()
    paths = []
    if cfg.log_paths is not None:
        for log_path in cfg.log_paths:
            paths.append(log_path.expanduser().resolve())

        # remove duplicates:
        cfg.log_paths = list(set(paths))
    cfg.base_config_path = cfg.base_config_path.expanduser().resolve()
    cfg.plot_config_path = cfg.base_config_path.expanduser().resolve()

    return cfg


def normalize_r_log_paths(cfg):
    # convert rellative paths to absolute paths
    if cfg.r_log_paths is not None:
        r_paths = []
        for r_log_path in cfg.r_log_paths:
            r_paths.append(r_log_path.expanduser().resolve())

        # remove duplicates:
        cfg.r_log_paths = list(set(r_paths))
