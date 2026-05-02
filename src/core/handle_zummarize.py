import subprocess


def call_zummarize(cfg):
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
    if cfg.zummarize_cli != []:
        return True
    for path in cfg.log_paths:
        if not (path / "zummary").exists():
            return True
    return False
