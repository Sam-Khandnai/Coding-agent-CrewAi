# ══════════════════════════════════════════════
# Tool 3 — Edit File
# ══════════════════════════════════════════════
from crewai.tools import BaseTool

from pathlib import Path


class EditFileTool(BaseTool):
    name: str = "edit_file"

    description: str = (
        "Finds exact text inside a file and replaces it with new text. "
        "Always read the file before editing it."
    )

    working_dir: Path

    def _run(
        self,
        file_path: str,
        old_text: str,
        new_text: str,
    ) -> str:

        root = self.working_dir.resolve()
        target = (root / file_path).resolve()

        if not target.is_relative_to(root):
            return "Error: Path is outside the project directory."

        if not target.is_file():
            return f"Error: File '{file_path}' was not found."

        try:
            content = target.read_text(encoding="utf-8")

            if old_text not in content:
                return (
                    "Error: The specified text was not found "
                    "in the file."
                )

            if content.count(old_text) > 1:
                return (
                    "Error: The specified text appears more than once. "
                    "Please provide a more specific text."
                )

            updated = content.replace(
                old_text,
                new_text,
                1,
            )

            target.write_text(
                updated,
                encoding="utf-8",
            )

            return (
                f"SUCCESS: File '{file_path}' "
                "was successfully edited."
            )

        except Exception as e:
            return f"Error while editing file: {e}"