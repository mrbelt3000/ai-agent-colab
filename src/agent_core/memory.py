from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class AgentMemory:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.state: dict[str, Any] = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "tasks": [],
            "facts": {},
        }

    def load(self) -> None:
        if not self.path.exists():
            return
        self.state = json.loads(self.path.read_text(encoding="utf-8"))

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self.state, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def add_task_record(self, task: str, result: dict[str, Any]) -> None:
        self.state.setdefault("tasks", []).append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "task": task,
                "result": result,
            }
        )

    def remember_fact(self, key: str, value: Any) -> None:
        self.state.setdefault("facts", {})[key] = value

