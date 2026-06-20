"""Charge les modules pédagogiques depuis content/modules/*.md."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

FRONTMATTER_DELIMITER = "---"


@dataclass
class Check:
    type: str
    message: str
    params: dict = field(default_factory=dict)


@dataclass
class Module:
    slug: str
    title: str
    description: str
    content_md: str
    checks: list[Check] = field(default_factory=list)


def _split_frontmatter(text: str, filename: str) -> tuple[dict, str]:
    if not text.startswith(FRONTMATTER_DELIMITER):
        raise ValueError(
            f"{filename} : frontmatter manquant (le fichier doit commencer par '---')."
        )
    parts = text.split(FRONTMATTER_DELIMITER, 2)
    if len(parts) < 3:
        raise ValueError(
            f"{filename} : frontmatter mal fermé (il faut deux lignes '---')."
        )
    _, raw_frontmatter, content_md = parts
    try:
        frontmatter = yaml.safe_load(raw_frontmatter) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"{filename} : YAML invalide dans le frontmatter — {exc}") from exc
    if not isinstance(frontmatter, dict):
        raise ValueError(f"{filename} : le frontmatter doit être un mapping YAML.")
    return frontmatter, content_md.strip()


def _build_checks(raw_checks: list, filename: str) -> list[Check]:
    checks = []
    for i, raw in enumerate(raw_checks):
        if not isinstance(raw, dict) or "type" not in raw or "message" not in raw:
            raise ValueError(f"{filename} : check #{i} sans 'type' ou 'message'.")
        params = {k: v for k, v in raw.items() if k not in ("type", "message")}
        checks.append(Check(type=raw["type"], message=raw["message"], params=params))
    return checks


def load_modules(modules_dir: Path) -> list[Module]:
    """Parse tous les .md de modules_dir, triés par nom de fichier."""
    modules = []
    for path in sorted(modules_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        frontmatter, content_md = _split_frontmatter(text, path.name)

        for required in ("title", "description"):
            if required not in frontmatter:
                raise ValueError(f"{path.name} : '{required}' manquant dans le frontmatter.")

        raw_checks = frontmatter.get("checks", [])
        if not isinstance(raw_checks, list):
            raise ValueError(f"{path.name} : 'checks' doit être une liste.")

        modules.append(
            Module(
                slug=path.stem,
                title=frontmatter["title"],
                description=frontmatter["description"],
                content_md=content_md,
                checks=_build_checks(raw_checks, path.name),
            )
        )
    return modules
