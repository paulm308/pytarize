import subprocess


def generate_zummary(zummarize_path, log_path):
    try:
        result = subprocess.run([zummarize_path, log_path])
        print(result)
    except subprocess.CalledProcessError as e:
        print("The program exited with an error:")
        print(e.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}")
