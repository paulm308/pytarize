import yaml


def write_dict_to_yaml(data: dict, filename):
    """
    Creates a new yaml file or overwrites an existing one and saves the configuration cfg in that file.

    Parameters:
    data (dict): The data that should be saved (only used for cfg or solver_style).
    filename: The path to the savefile.
    """
    try:
        with open(filename, "w", encoding="utf-8") as outfile:
            # default_flow_style=False ensures readable block-style YAML
            yaml.dump(data, outfile, default_flow_style=False)
        print(f"YAML successfully written to {filename}")
    except OSError as e:
        print(f"Failed to write file: {e}")


def save_config(cfg):
    """
    Saves the configuration cfg in a yaml file.

    Parameters:
    cfg: The configuration.
    """
    if cfg.save_config is not None:
        write_dict_to_yaml(cfg.atr, cfg.save_config)


def save_solver_style(cfg):
    """
    Only saves the solver_style. The rest of the config file remains unchanged.

    Paramters:
    cfg: The configuration.
    """
    if cfg.save_config is not None:
        with open(cfg.save_config, "r") as file:
            data = yaml.safe_load(file)
            data["solver_style"] = cfg.atr["solver_style"]
            write_dict_to_yaml(data, cfg.save_config)
