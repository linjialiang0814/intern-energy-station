"""Validate that LLM calls safely fall back when no API key is configured."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services.llm_service import call_llm


def main() -> int:
    previous = os.environ.pop("ARK_API_KEY", None)
    try:
        result = call_llm(
            [{"role": "user", "content": "请用一句话说明实习生成长建议。"}],
            fallback="fallback-ok",
        )
    finally:
        if previous is not None:
            os.environ["ARK_API_KEY"] = previous

    checks = {
        "content_is_fallback": result.content == "fallback-ok",
        "used_fallback": result.used_fallback is True,
        "provider_is_fallback": result.provider == "fallback",
    }
    for name, passed in checks.items():
        print(f"{name}: {passed}")
    print("error:", result.error)
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
