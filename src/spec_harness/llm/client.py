"""LLM client for natural language spec generation."""

import json
import os
from typing import Any

import httpx

from spec_harness.config import HarnessConfig


class LLMClient:
    """OpenAI-compatible LLM client for spec generation."""

    def __init__(self, config: HarnessConfig):
        self.config = config
        self.base_url = config.llm.base_url or os.getenv(
            "OPENAI_BASE_URL", "https://api.openai.com/v1"
        )
        self.api_key = config.llm.api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = config.llm.model or "gpt-4.1"

    def is_available(self) -> bool:
        return bool(self.api_key) and bool(self.base_url)

    def generate(self, prompt: str, temperature: float = 0.3, max_tokens: int = 4000) -> str:
        if not self.is_available():
            raise RuntimeError(
                "LLM not configured. Set OPENAI_API_KEY or configure llm.api_key in harness.yaml."
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self._system_prompt()},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=120.0,
        )
        response.raise_for_status()
        data = response.json()
        return str(data["choices"][0]["message"]["content"])

    def generate_json(self, prompt: str, temperature: float = 0.2) -> dict[str, Any]:
        content = self.generate(prompt, temperature=temperature)
        # Extract JSON from markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return dict(json.loads(content))

    def _system_prompt(self) -> str:
        result: str = (
            "You are a senior software requirements analyst and "
            "technical writer. "
            "Your job is to convert vague business requirements into "
            "precise, structured software engineering artifacts. "
            "Always produce well-structured output. "
            "Prefer specific, actionable language over vague terms. "
            "When generating user stories, use standard format: "
            "As a [role], I want to [action], so that [value]."
        )
        return result
