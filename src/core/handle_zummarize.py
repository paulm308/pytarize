import subprocess


def call_zummarize(cfg):
    """
    Calls the zummarize script with all extracted and normalized paths, the zummarize arguments
    and prints the result.

    Parameters:
    cfg: The configuration.
    """
    try:
        print([cfg.zummarize_path] + cfg.zummarize_cli + cfg.log_paths)
        result = subprocess.run([cfg.zummarize_path] + cfg.zummarize_cli + cfg.log_paths)
        print(result)
    except subprocess.CalledProcessError as e:
        print("The program exited with an error:")
        print(e.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}")


def zummarize_required(cfg):
    """
    Checks if a call to the zummarize script is required. This is the case if one path does not contain a zummary
    or if zummarize specific options are used.

    Parameters:
    cfg: The configuration.

    Returns:
    bool: True if zummarize is required, else False.
    """
    copy_cli = cfg.zummarize_cli[:]
    for opt in ["--sat", "--unsat"]:
        if opt in copy_cli:
            copy_cli.remove(opt)
    if copy_cli != []:
        return True
    for path in cfg.log_paths:
        if not (path / "zummary").exists():
            return True
    return False
