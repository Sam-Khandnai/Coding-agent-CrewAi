# ══════════════════════════════════════════════
# Tool 2 — Read File
# ══════════════════════════════════════════════
from crewai.tools import BaseTool

from pathlib import Path


class ReadFileTool(BaseTool):
    name: str = "read_file"

    description: str = (
        "Reads the content of a text file inside the project."
    )

    working_dir: Path

    def _run(self, file_path: str) -> str:
        root = self.working_dir.resolve()
        target = (root / file_path).resolve()

        if not target.is_relative_to(root):
            return "Error: Path is outside the project directory."

        if not target.is_file():
            return f"Error: File '{file_path}' was not found."

        try:
            return target.read_text(encoding="utf-8")

        except Exception as e:
            return f"Error while reading file: {e}"