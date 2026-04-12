import subprocess


def generate_zummary(ncfg):
    try:
        result = subprocess.run([ncfg.zummarize_path, ncfg.log_path])
        print(result)
    except subprocess.CalledProcessError as e:
        print("The program exited with an error:")
        print(e.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}")
