import subprocess
from typing import List, Optional


def expand_with_bash(value: Optional[str]) -> List[str]:
    if value is None:
        return []

    # printf '%s\n' gibt jedes expandierte Wort auf einer eigenen Zeile aus
    result = subprocess.run(
        ["bash", "-c", f'printf "%s\\n" {value}'],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in result.stdout.splitlines() if line]
