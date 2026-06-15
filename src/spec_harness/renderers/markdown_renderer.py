"""Markdown and YAML rendering utilities."""

from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape


class MarkdownRenderer:
    """Render structured data to Markdown using Jinja2 templates."""

    def __init__(self, templates_dir: Path):
        self.env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, template_name: str, data: dict[str, Any]) -> str:
        template = self.env.get_template(template_name)
        return template.render(**data)

    def render_to_file(self, template_name: str, data: dict[str, Any], output_path: Path) -> None:
        content = self.render(template_name, data)
        output_path.write_text(content, encoding="utf-8")


class YamlRenderer:
    """Render structured data to YAML files."""

    def render(self, data: dict[str, Any], output_path: Path) -> None:
        # Custom representer to preserve string types for numeric strings
        def str_representer(dumper, data):
            if isinstance(data, str) and data.isdigit():
                return dumper.represent_scalar('tag:yaml.org,2002:str', data)
            return dumper.represent_scalar('tag:yaml.org,2002:str', data)

        yaml.add_representer(str, str_representer)

        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    def render_to_string(self, data: dict[str, Any]) -> str:
        def str_representer(dumper, data):
            if isinstance(data, str) and data.isdigit():
                return dumper.represent_scalar('tag:yaml.org,2002:str', data)
            return dumper.represent_scalar('tag:yaml.org,2002:str', data)

        yaml.add_representer(str, str_representer)
        return yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)
