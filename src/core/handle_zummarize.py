import subprocess


def call_zummarize(cfg):
    try:
        result = subprocess.run([cfg.zummarize_path] + cfg.log_paths)
        print(result)
    except subprocess.CalledProcessError as e:
        print("The program exited with an error:")
        print(e.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}")
