
# ══════════════════════════════════════════════
# Create and Run Agent
# ══════════════════════════════════════════════
from crewai.tools import BaseTool
from crewai import Agent , Task, Process , Crew , LLM 
from pathlib import Path

from coding_agent.configs import OPENROUTER_API_KEY , OPENROUTER_MODEL 
from tools import Edit_File , List_Files , Read_File , Run_py_Code



def run_agent(request: str, working_dir: Path) -> str:

    if not OPENROUTER_API_KEY:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not configured. "
            "Please add it to the .env file."
        )

    # Connect to the model through OpenRouter
    llm = LLM(
        model=f"openrouter/{OPENROUTER_MODEL}",
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.1,
    )

    # Define tools
    tools = [
        List_Files.ListFilesTool(working_dir=working_dir),
        Read_File.ReadFileTool(working_dir=working_dir),
        Edit_File.EditFileTool(working_dir=working_dir),
        Run_py_Code.RunPythonTool(working_dir=working_dir),
    ]
    # Define agent
    agent = Agent(
        role="Senior Software Engineer",

        goal=(
            "Find bugs, edit the necessary files, "
            "and verify the result."
        ),

        backstory=(
            "You are a senior software engineer. "
            "You only work inside the WorkingDir. "
            "Before making any edit, read the file first. "
            "After every change, run the code to verify that it works."
        ),

        llm=llm,
        tools=tools,
        verbose=True,
        allow_delegation=False,
        max_iter=15,
    )

    # Define task
    task = Task(
        description=(
            f"Working directory:\n{working_dir}\n\n"
            f"User request:\n{request}\n\n"

            "Required workflow:\n"
            "1. Inspect the project structure using list_project_files.\n"
            "2. Read the relevant files using read_file.\n"
            "3. Diagnose the root cause before editing.\n"
            "4. Apply the required changes using edit_file.\n"
            "5. Verify the changes using run_python.\n"
            "6. Never claim that a file was edited unless edit_file "
            "returned SUCCESS.\n"
            "7. Never claim that a test passed unless run_python "
            "returned STATUS: SUCCESS.\n"
            "8. Provide a final report based only on actual tool results."
        ),

        expected_output=(
            "A report containing: the root cause, "
            "modified files, applied changes, "
            "and final test results."
        ),

        agent=agent,
        tools=tools,
    )

    # Run crew
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    return getattr(result, "raw", str(result))