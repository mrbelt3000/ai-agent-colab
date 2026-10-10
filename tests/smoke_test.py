from __future__ import annotations

import tempfile
from pathlib import Path

from agent_core.agent import WorkAgent
from agent_core.config import AgentConfig


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        config = AgentConfig(
            name="Smoke Test Agent",
            mode="controlled",
            max_steps_per_task=4,
            workspace_root=root,
            drive_root=root / "drive",
            memory_file=root / "drive" / "memory" / "state.json",
            log_file=root / "drive" / "logs" / "agent.log",
            permissions={
                "allow_file_read": True,
                "allow_file_write": True,
                "allow_python_execution": True,
                "allow_shell_execution": False,
                "allow_git_push": False,
            },
            model={"provider": "placeholder"},
        )
        agent = WorkAgent(config)
        agent.start()
        result = agent.handle_task("Create a tiny game.")
        project = agent.create_text_project("projects/demo", "Demo Game")

        assert result["status"] == "planned"
        assert "run_python" in result["available_tools"]
        assert (root / "projects" / "demo" / "main.py").exists()
        assert "Demo Game" in project["test_output"]
        assert config.memory_file.exists()
        assert config.log_file.exists()

    print("Smoke test passed.")


if __name__ == "__main__":
    main()

