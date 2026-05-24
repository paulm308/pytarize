import yaml


def write_dict_to_yaml(data: dict, filename):
    try:
        with open(filename, "w", encoding="utf-8") as outfile:
            # default_flow_style=False ensures readable block-style YAML [InlineCitation-1-python - How can I write data in YAML format in a file? - Stack Overflow](https://stackoverflow.com/questions/12470665/how-can-i-write-data-in-yaml-format-in-a-file)
            yaml.dump(data, outfile, default_flow_style=False)
        print(f"YAML successfully written to {filename}")
    except OSError as e:
        print(f"Failed to write file: {e}")


def save_config(cfg):
    if cfg.save_config is not None:
        write_dict_to_yaml(cfg.atr, cfg.save_config)
