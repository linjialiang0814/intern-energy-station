"""Run all project validation checks before deployment."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

VALIDATION_SCRIPTS = [
    "validate_rules.py",
    "validate_dashboard_data.py",
    "validate_ai_features.py",
    "validate_llm_fallback.py",
    "validate_score_explanations.py",
    "validate_exports.py",
]


def run_command(command: list[str]) -> bool:
    print(f"\n$ {' '.join(command)}")
    completed = subprocess.run(command, cwd=ROOT, text=True)
    return completed.returncode == 0


def collect_python_files() -> list[str]:
    files = [ROOT / "app.py"]
    for folder in ["pages", "services", "scripts"]:
        files.extend(sorted((ROOT / folder).glob("*.py")))
    return [str(path) for path in files]


def main() -> int:
    checks: list[tuple[str, list[str]]] = []
    for script in VALIDATION_SCRIPTS:
        checks.append((script, [sys.executable, str(ROOT / "scripts" / script)]))

    checks.append(("py_compile", [sys.executable, "-m", "py_compile", *collect_python_files()]))

    failed = []
    for name, command in checks:
        if not run_command(command):
            failed.append(name)

    print("\n=== Quality Check Summary ===")
    if failed:
        print(f"FAILED: {', '.join(failed)}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
