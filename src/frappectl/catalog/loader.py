from pathlib import Path

import yaml

from frappectl.catalog.models import AppDefinition


def _load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data


def load_catalog(path: str | None = None) -> dict:
    catalog_path = Path(path) if path else Path(__file__).with_name("default_apps.yaml")
    return _load_yaml(catalog_path)


def parse_app_list(items: list[dict] | None) -> list[AppDefinition]:
    apps: list[AppDefinition] = []
    for item in items or []:
        apps.append(
            AppDefinition(
                name=item["name"],
                repo=item["repo"],
                branch=item.get("branch"),
                category=item.get("category", "custom"),
            )
        )
    return apps