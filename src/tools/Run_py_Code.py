# ══════════════════════════════════════════════
# Tool 4 — Run Python Code
# ══════════════════════════════════════════════
from crewai.tools import BaseTool
import subprocess
import sys

from pathlib import Path


class RunPythonTool(BaseTool):
    name: str = "run_python"

    description: str = (
        "Runs a Python script inside the project and returns its output. "
        "The script_path must be a relative path to a .py file. "
        "Do not put Python source code inside script_path."
    )

    working_dir: Path

    def _run(self, script_path: str) -> str:
        root = self.working_dir.resolve()
        target = (root / script_path).resolve()

        if not target.is_relative_to(root):
            return "Error: Path is outside the project directory."

        if not target.is_file():
            return f"Error: File '{script_path}' was not found."

        if target.suffix.lower() != ".py":
            return "Error: Only .py files can be executed."

        try:
            result = subprocess.run(
                [sys.executable, str(target)],
                cwd=str(root),
                capture_output=True,
                text=True,
                timeout=30,
            )

            status = (
                "SUCCESS"
                if result.returncode == 0
                else "FAILED"
            )

            return (
                f"STATUS: {status}\n"
                f"RETURN CODE: {result.returncode}\n\n"
                f"OUTPUT:\n{result.stdout}\n"
                f"ERRORS:\n{result.stderr}"
            )

        except subprocess.TimeoutExpired:
            return (
                "STATUS: FAILED\n"
                "Error: Execution timed out after 30 seconds."
            )

        except Exception as e:
            return f"STATUS: FAILED\nError: {e}"