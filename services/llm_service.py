"""Unified LLM access with Volcengine Ark support and safe fallback."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import requests


DEFAULT_ARK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
DEFAULT_ARK_MODEL = "doubao-seed-2-0-lite-260215"


@dataclass(frozen=True)
class LLMConfig:
    provider: str
    api_key: str
    base_url: str
    model: str
    timeout_seconds: int = 20


@dataclass(frozen=True)
class LLMResult:
    content: str
    provider: str
    model: str
    used_fallback: bool
    error: str = ""


def _get_secret_value(key: str, default: str = "") -> str:
    """Read a config value from env first, then Streamlit secrets if available."""
    env_value = os.getenv(key)
    if env_value:
        return env_value

    try:
        import streamlit as st

        if key in st.secrets:
            return str(st.secrets[key])
        llm_section = st.secrets.get("llm", {})
        if key in llm_section:
            return str(llm_section[key])
    except Exception:
        return default

    return default


def load_llm_config() -> LLMConfig | None:
    """Load Volcengine Ark config, returning None when no API key is configured."""
    api_key = (
        _get_secret_value("ARK_API_KEY")
        or _get_secret_value("VOLCENGINE_ARK_API_KEY")
        or _get_secret_value("VOLCENGINE_API_KEY")
    )
    if not api_key:
        return None

    base_url = _get_secret_value("ARK_BASE_URL", DEFAULT_ARK_BASE_URL).rstrip("/")
    model = _get_secret_value("ARK_MODEL", DEFAULT_ARK_MODEL)
    timeout_raw = _get_secret_value("LLM_TIMEOUT_SECONDS", "20")
    try:
        timeout_seconds = max(5, int(timeout_raw))
    except ValueError:
        timeout_seconds = 20

    return LLMConfig(
        provider="volcengine-ark",
        api_key=api_key,
        base_url=base_url,
        model=model,
        timeout_seconds=timeout_seconds,
    )


def _chat_url(base_url: str) -> str:
    if base_url.endswith("/chat/completions"):
        return base_url
    return f"{base_url}/chat/completions"


def call_llm(
    messages: list[dict[str, str]],
    fallback: str,
    *,
    temperature: float = 0.2,
    max_tokens: int = 800,
) -> LLMResult:
    """Call the configured LLM, or return fallback content when unavailable."""
    config = load_llm_config()
    if config is None:
        return LLMResult(
            content=fallback,
            provider="fallback",
            model="rules-template",
            used_fallback=True,
            error="ARK_API_KEY is not configured",
        )

    payload: dict[str, Any] = {
        "model": config.model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    headers = {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            _chat_url(config.base_url),
            headers=headers,
            json=payload,
            timeout=config.timeout_seconds,
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"].strip()
        if not content:
            raise ValueError("empty LLM response")
        return LLMResult(
            content=content,
            provider=config.provider,
            model=config.model,
            used_fallback=False,
        )
    except Exception as exc:
        return LLMResult(
            content=fallback,
            provider=config.provider,
            model=config.model,
            used_fallback=True,
            error=str(exc),
        )
