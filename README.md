# Coding Agent

> An educational, tool-using Coding Agent built with **CrewAI** and **OpenRouter**.

A lightweight Coding Agent that can inspect a project, read source files, modify them, execute Python scripts, and report the results.

The project is designed primarily as a **learning project for Agentic AI**, demonstrating how an LLM can interact with a real codebase through controlled tools instead of simply generating code in a chat interface.

---

## Features

* Inspect a project's directory structure
* Read source files
* Edit files using exact text replacement
* Execute Python scripts
* Automatically verify changes
* Work with any OpenRouter-supported model
* Interactive terminal interface
* Direct request mode
* Project-directory access restriction
* Educational and modular architecture

### Available Tools

| Tool                 | Purpose                                                |
| -------------------- | ------------------------------------------------------ |
| `list_project_files` | Lists files and directories inside the working project |
| `read_file`          | Reads the content of a file                            |
| `edit_file`          | Replaces a specific piece of text inside a file        |
| `run_python`         | Executes a Python script and returns its output        |

The tools are implemented as CrewAI `BaseTool` classes and are provided directly to the agent.

---

## How It Works

The basic architecture is:

```text
                  ┌─────────────────────┐
                  │       User          │
                  │  Coding Request     │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │    CrewAI Agent     │
                  │ Senior Software     │
                  │ Engineer            │
                  └──────────┬──────────┘
                             │
                    Tool Calling
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
   ┌────────────┐     ┌────────────┐     ┌────────────┐
   │ List Files │     │ Read File  │     │ Edit File  │
   └────────────┘     └────────────┘     └────────────┘
                                                │
                                                ▼
                                         ┌────────────┐
                                         │Run Python  │
                                         └────────────┘
                                                │
                                                ▼
                                         Verification
                                                │
                                                ▼
                                         Final Report
```

The agent is instructed to follow a specific development workflow:

```text
1. Inspect project
        ↓
2. Read relevant files
        ↓
3. Understand the problem
        ↓
4. Edit required files
        ↓
5. Run Python code
        ↓
6. Verify the result
        ↓
7. Generate final report
```

This workflow is explicitly defined inside the CrewAI task.

---

# Project Structure

```text
coding-agent/
│
├── calculator/
│
├── src/
│   └── coding_agent/
│       ├── __init__.py
│       ├── Agent_Task.py
│       ├── configs.py
│       └── Interactive_Loop.py    
│
├── tools/
│   ├── __init__.py
│   ├── Edit_File.py
│   ├── List_File.py
│   ├── Read_File.py
│   └── Run_Py_Code.py
│
├── README.md
├── .env
├── main.py
└── pyproject.toml
```

### `src/coding_agent/`

Contains the main application package.

### `agent.py`

Responsible for defining the Coding Agent, its LLM configuration, tools, tasks, and CrewAI execution flow.

### `prompts.py`

Contains prompt templates and instructions used to control the agent's behavior.

Keeping prompts separate from the agent implementation makes it easier to experiment with different agent behaviors without changing the core logic.

### `tools.py`

Contains the custom tools available to the agent.

The educational implementation provides four core tools:

```text
ListFilesTool
ReadFileTool
EditFileTool
RunPythonTool
```

### `pyproject.toml`

Contains project metadata and Python dependencies.

### `.env`

Stores environment variables such as the OpenRouter API key and model name.

> **Important:** Never commit your real `.env` file or API key to GitHub.

---

# Requirements

* Python 3.10+
* [CrewAI](https://github.com/crewAIInc/crewAI)
* OpenRouter API key
* `uv`

The project uses environment variables to configure the OpenRouter connection.

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/Sam-Khandnai/Coding-agent-CrewAi.git
cd coding-agent
```

## 2. Install dependencies

If the project is configured with `uv`:

```bash
uv sync
```

## 3. Configure environment variables

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=openrouter/free

```

You can replace the model with another model available through OpenRouter.

The application loads these values using `python-dotenv`.

---

# Usage

The agent receives the **Working Directory** as its first argument.

## Interactive Mode

Run:

```bash
uv run main.py "PATH_TO_PROJECT"
```

For example:

```bash
uv run main.py ".\calculator"
```

You will then see:

```text
============================================================
  Coding Agent | CrewAI + OpenRouter
============================================================
Project: F:\my\projects\calculator
Model:   openrouter/free


Type 'exit' to quit.

Request >
```

You can now provide a request:

```text
Request > Find the bug in the calculator project and fix it.
```

The agent will inspect the project, read relevant files, make changes, run Python code, and return a final report.

---

# Direct Execution Mode

You can also provide the request directly from the command line:

```bash
uv run main.py "PATH_TO_PROJECT" "YOUR REQUEST"
```

Example:

```bash
uv run main.py ".\calculator" "Find and fix the bug in this project"
```

The CLI supports both an optional `request` argument and interactive mode.

---

# Example Requests

### Debugging

```text
Find and fix the bug in this project.
```

### Code Analysis

```text
Analyze this project and explain how it works.
```

### Refactoring

```text
Refactor the calculator code to make it cleaner.
```

### Feature Development

```text
Add input validation to the calculator.
```

### Project Summary

```text
Give me a summary of this project explaining exactly what it does.
```

The agent can decide which files it needs to inspect before taking action.

---

# The Four Tools

## 1. List Project Files

```python
list_project_files
```

This tool allows the agent to understand the structure of the project.

Example:

```text
[DIR] src
[DIR] tests
[FILE] README.md
[FILE] main.py
[FILE] pyproject.toml
```

The tool also hides common unnecessary directories such as:

```text
.git
.venv
__pycache__
node_modules
```

This keeps the agent's view of the project cleaner.

---

## 2. Read File

```python
read_file
```

After discovering the project structure, the agent can read relevant files.

For example:

```text
read_file("src/calculator.py")
```

The tool reads the file using UTF-8 encoding.

---

## 3. Edit File

```python
edit_file
```

The editing tool uses **exact text replacement**.

It receives:

```text
file_path
old_text
new_text
```

Before modifying a file, the agent is instructed to read it first.

The tool also prevents ambiguous replacements by rejecting an `old_text` value if it appears multiple times in the file.

Conceptually:

```text
old code
   │
   ▼
Find exact text
   │
   ▼
Replace once
   │
   ▼
Write updated file
```

This is intentionally simple and makes the editing mechanism easy to understand.

---

## 4. Run Python

```python
run_python
```

The agent can execute Python scripts inside the working directory.

The tool:

* Only accepts `.py` files
* Uses the current Python interpreter
* Captures stdout
* Captures stderr
* Returns the execution status
* Has a 30-second timeout

For example:

```text
run_python("main.py")
```

The result contains:

```text
Status: Success

Output:
...

Errors:
...
```

---

# Agent Configuration

The agent is configured with the role:

```text
Senior Software Engineer
```

Its main objective is:

```text
Find bugs, edit the necessary files, and verify the result.
```

It is also explicitly instructed to:

```text
Only work inside the WorkingDir.

Read a file before editing it.

Run the code after making changes.
```

The agent currently uses:

```python
temperature=0.1
```

and:

```python
max_iter=15
```

This keeps the model's responses relatively deterministic while giving it enough iterations to inspect, modify, and verify a project.

---

# OpenRouter Integration

The project uses OpenRouter as the model provider.

The LLM is configured with:

```python
LLM(
    model=f"openrouter/{OPENROUTER_MODEL}",
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.1,
)
```

This means the agent architecture is largely independent of the underlying model.

You can change:

```env
OPENROUTER_MODEL=...
```

without changing the agent implementation.

---

# Why Tools Matter in Agentic AI

A normal LLM interaction looks like:

```text
User
  ↓
LLM
  ↓
Text Response
```

A tool-using agent looks more like:

```text
User
  ↓
LLM
  ↓
Decision
  ↓
Tool
  ↓
Tool Result
  ↓
LLM
  ↓
Decision
  ↓
Tool
  ↓
...
  ↓
Final Answer
```

This distinction is one of the most important concepts in **Agentic AI**.

The LLM itself does not directly "know" the contents of your project.

Instead, it has access to tools that allow it to:

```text
Observe → Reason → Act → Observe → Verify
```

This project demonstrates that loop using a real filesystem and Python execution environment.

---

# Security Considerations

The tools are intentionally restricted to the configured `WorkingDir`.

Before accessing a file or directory, the implementation resolves the path and checks that it remains inside the working directory.

For example:

```text
WorkingDir/
│
├── src/
├── tests/
└── main.py
```

The agent should not be able to use:

```text
../some-other-directory
```

to escape the project directory.

The same boundary check is applied to the file-listing, file-reading, editing, and Python execution tools.

> **Warning:** This is an educational project, not a production-grade sandbox. Running arbitrary Python code from an AI agent can be dangerous. Only use it with projects and environments you trust.

---

# Educational Concepts

This project is useful for learning several important Agentic AI concepts:

### 1. LLM Tool Calling

How an LLM can select and use external tools.

### 2. Agent Architecture

How an agent can combine:

```text
LLM
+
Instructions
+
Tools
+
Task
```

to perform multi-step work.

### 3. Agentic Workflow

Instead of generating an answer immediately, the agent follows:

```text
Inspect
  ↓
Read
  ↓
Reason
  ↓
Edit
  ↓
Execute
  ↓
Verify
  ↓
Report
```

### 4. Environment Configuration

API keys and model configuration are separated from the application using `.env`.

### 5. Controlled File Access

The agent does not receive unrestricted filesystem access.

### 6. Verification

The agent does not simply modify code and stop. It is instructed to execute the result and verify the changes.

---

# CrewAI Workflow

The project uses a single CrewAI agent and a sequential Crew.

Conceptually:

```text
Crew
 │
 └── Agent
      │
      └── Task
           │
           ├── Inspect project
           ├── Read files
           ├── Edit files
           ├── Run Python
           └── Generate report
```

The Crew is configured with:

```python
process=Process.sequential
```

and executes the defined task through `crew.kickoff()`.

---

# Limitations

This project intentionally keeps the architecture simple.

Current limitations include:

* Python-focused execution
* No terminal/shell tool
* No Git integration
* No automated test framework integration
* No persistent agent memory
* No vector database or RAG
* No multi-agent collaboration
* No production-grade sandbox
* File editing is based on exact text replacement
* Python execution has a fixed 30-second timeout

These limitations are intentional because the main goal is to demonstrate the fundamentals of a tool-using Coding Agent.

---

# Future Improvements

Possible extensions include:

* [ ] Add a terminal/shell tool
* [ ] Add Git/GitHub integration
* [ ] Add automated test detection
* [ ] Add test execution
* [ ] Add code search
* [ ] Add AST-based code editing
* [ ] Add project indexing
* [ ] Add RAG over the codebase
* [ ] Add persistent memory
* [ ] Add multi-agent architecture
* [ ] Add Docker-based execution sandbox
* [ ] Add human approval before file modifications
* [ ] Add structured execution logs
* [ ] Add support for JavaScript/TypeScript projects
* [ ] Add FastAPI backend
* [ ] Add web-based interface

---

# Learning Path

If you are studying Agentic AI, a good progression after this project is:

```text
LLM API
   ↓
Prompt Engineering
   ↓
Tool Calling
   ↓
Single Agent
   ↓
Agent + Multiple Tools
   ↓
Planning
   ↓
Memory
   ↓
RAG
   ↓
Multi-Agent Systems
   ↓
MCP
   ↓
Production Agent Architecture
```

This project sits around the:

```text
Tool Calling → Single Agent → Multi-Tool Agent
```

stage.

---

# Tech Stack

| Technology    | Purpose                           |
| ------------- | --------------------------------- |
| Python        | Core programming language         |
| CrewAI        | Agent orchestration               |
| OpenRouter    | LLM API provider                  |
| python-dotenv | Environment configuration         |
| uv            | Dependency and project management |

---

# Project Goal

The goal of this project is **not** to build another ChatGPT clone.

The goal is to understand how an LLM can become an actual software-engineering agent by giving it controlled capabilities to:

```text
Understand a project
        ↓
Inspect files
        ↓
Read code
        ↓
Modify code
        ↓
Execute code
        ↓
Verify changes
```

This is the fundamental idea behind a tool-using Coding Agent.

---

# License

This project is intended for educational purposes.

Add your preferred license here, for example:

```text
MIT License
```

---

## Author

**Sam Khandani**

AI Agent Engineer | ML/DL Engineer | AI Engineer

GitHub: `@Sam-Khandnai`
