"""Configuration management for the harness."""

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class ProjectConfig(BaseModel):
    name: str = "spec-driven-ai-coding-harness"
    output_dir: str = "outputs"


class GenerationConfig(BaseModel):
    mode: str = "rule_based"  # rule_based or llm
    language: str = "en"
    output_formats: list[str] = Field(default_factory=lambda: ["markdown", "yaml"])


class LLMConfig(BaseModel):
    provider: str = "openai_compatible"
    model: str = "gpt-4.1"
    base_url: str | None = None
    api_key: str | None = None


class TestingConfig(BaseModel):
    generate_pytest: bool = True
    generate_playwright: bool = True


class QualityGatesConfig(BaseModel):
    require_acceptance_criteria: bool = True
    require_test_cases: bool = True
    require_task_traceability: bool = True


class HarnessConfig(BaseModel):
    project: ProjectConfig = Field(default_factory=ProjectConfig)
    generation: GenerationConfig = Field(default_factory=GenerationConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    testing: TestingConfig = Field(default_factory=TestingConfig)
    quality_gates: QualityGatesConfig = Field(default_factory=QualityGatesConfig)

    @classmethod
    def load(cls, path: str = "harness.yaml") -> "HarnessConfig":
        import yaml

        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            # Resolve environment variables in strings
            data = _resolve_env_vars(data)
            return cls(**data)
        return cls()

    def get_output_dir(self) -> Path:
        return Path(self.project.output_dir)


def _resolve_env_vars(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _resolve_env_vars(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_resolve_env_vars(v) for v in obj]
    elif isinstance(obj, str) and obj.startswith("${") and obj.endswith("}"):
        env_var = obj[2:-1]
        return os.getenv(env_var, obj)
    return obj
