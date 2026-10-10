from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class AgentConfig:
    name: str
    mode: str
    max_steps_per_task: int
    workspace_root: Path
    drive_root: Path
    memory_file: Path
    log_file: Path
    permissions: dict[str, Any]
    model: dict[str, Any]


def load_config(path: str | Path) -> AgentConfig:
    config_path = Path(path)
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    paths = raw["paths"]
    drive_root = Path(paths["drive_root"])

    return AgentConfig(
        name=raw["agent"]["name"],
        mode=raw["agent"]["mode"],
        max_steps_per_task=int(raw["agent"]["max_steps_per_task"]),
        workspace_root=Path(paths["workspace_root"]),
        drive_root=drive_root,
        memory_file=drive_root / paths["memory_file"],
        log_file=drive_root / paths["log_file"],
        permissions=raw["permissions"],
        model=raw["model"],
    )

