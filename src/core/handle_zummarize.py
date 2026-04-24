import subprocess


def call_zummarize(cfg):
    try:
        result = subprocess.run([cfg.zummarize_path] + cfg.log_paths + cfg.zummarize_cli)
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
