# ══════════════════════════════════════════════
# Tool 1 — List Files
# ══════════════════════════════════════════════
from crewai.tools import BaseTool

from pathlib import Path

class ListFilesTool(BaseTool):

    name: str = "list_project_files"

    description: str = (
        "Lists files and directories inside the project. "
        "To inspect a subdirectory, provide a relative path, "
        "for example 'src'."
    )

    working_dir: Path

    def _run(self, path: str = ".") -> str:
            root = self.working_dir.resolve()
            target = (root / path).resolve()

            # Prevent access outside the project directory
            if not target.is_relative_to(root):
                return "Error: Path is outside the project directory."

            if not target.is_dir():
                return f"Error: Directory '{path}' was not found."

            lines = []

            for item in sorted(
                target.iterdir(),
                key=lambda p: (not p.is_dir(), p.name.lower())
            ):
                if item.name in {
                    "__pycache__",
                    ".git",
                    ".venv",
                    "venv",
                    "node_modules",
                }:
                    continue

                prefix = "[DIR] " if item.is_dir() else "[FILE]"
                lines.append(
                    f"{prefix} {item.relative_to(root)}"
                )

            return "\n".join(lines) if lines else "Directory is empty."

