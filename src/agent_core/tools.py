from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


ToolHandler = Callable[..., str]


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    handler: ToolHandler


class ToolRegistry:
    def __init__(self, workspace_root: str | Path) -> None:
        self.workspace_root = Path(workspace_root).resolve()
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def names(self) -> list[str]:
        return sorted(self._tools)

    def run(self, name: str, **kwargs: str) -> str:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        return self._tools[name].handler(**kwargs)

    def safe_path(self, relative_path: str) -> Path:
        target = (self.workspace_root / relative_path).resolve()
        if self.workspace_root not in target.parents and target != self.workspace_root:
            raise ValueError(f"Path escapes workspace: {relative_path}")
        return target


def build_default_tools(workspace_root: str | Path, log_file: str | Path) -> ToolRegistry:
    registry = ToolRegistry(workspace_root)
    log_path = Path(log_file)

    def list_dir(path: str = ".") -> str:
        target = registry.safe_path(path)
        if not target.exists():
            return f"Missing directory: {path}"
        if not target.is_dir():
            return f"Not a directory: {path}"
        return "\n".join(sorted(item.name for item in target.iterdir()))

    def read_file(path: str) -> str:
        target = registry.safe_path(path)
        return target.read_text(encoding="utf-8")

    def write_file(path: str, content: str) -> str:
        target = registry.safe_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"Wrote {path}"

    def run_python(path: str) -> str:
        target = registry.safe_path(path)
        completed = subprocess.run(
            ["python", str(target)],
            cwd=registry.workspace_root,
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
        output = completed.stdout.strip()
        error = completed.stderr.strip()
        return "\n".join(part for part in [output, error] if part)

    def append_log(message: str) -> str:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(message.rstrip() + "\n")
        return "Logged"

    registry.register(Tool("list_dir", "List files in a workspace directory.", list_dir))
    registry.register(Tool("read_file", "Read a UTF-8 text file.", read_file))
    registry.register(Tool("write_file", "Write a UTF-8 text file.", write_file))
    registry.register(Tool("run_python", "Run a Python file inside the workspace.", run_python))
    registry.register(Tool("append_log", "Append a line to the persistent agent log.", append_log))
    return registry

