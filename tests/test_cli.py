"""Tests for CLI commands."""

from pathlib import Path
from typer.testing import CliRunner

from spec_harness.cli import app

runner = CliRunner()


def test_init_command(tmp_path: Path):
    import os
    os.chdir(tmp_path)
    result = runner.invoke(app, ["init", "--name", "test-project"])
    assert result.exit_code == 0
    assert (tmp_path / "harness.yaml").exists()
    assert (tmp_path / "requirements").exists()


def test_init_creates_harness_yaml(tmp_path: Path):
    import os
    os.chdir(tmp_path)
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    content = (tmp_path / "harness.yaml").read_text(encoding="utf-8")
    assert "spec-driven-ai-coding-harness" in content or "project:" in content


def test_validate_missing_dir(tmp_path: Path):
    import os
    os.chdir(tmp_path)
    result = runner.invoke(app, ["validate", "nonexistent/"])
    assert result.exit_code != 0


def test_validate_with_empty_dir(tmp_path: Path):
    import os
    os.chdir(tmp_path)
    (tmp_path / "outputs").mkdir()
    result = runner.invoke(app, ["validate", "outputs/"])
    assert result.exit_code != 0
