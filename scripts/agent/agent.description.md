# Description

## Agent: Orchestrates work among sub-agents for code improvement

This module provides the main Agent that coordinates the improvement process across code files by
calling specialized sub-agents for different aspects of code quality and documentation.

## Key Features

- Orchestrates multiple specialized agents for code improvement

- Supports iterative improvement loops with change detection

- Handles git operations for version control

- Processes files in batches with configurable limits

- Provides comprehensive progress reporting

## Architecture

The Agent class coordinates the following sub-agents:

- agent-context: Improves documentation and descriptions

- agent-changes: Manages changelog updates

- agent-errors: Analyzes and reports errors

- agent-improvements: Suggests code improvements

- agent-tests: Manages test suite development

- agent-coder: Performs code refactoring and improvements

- agent-stats: Provides progress reporting

## Usage

```python
agent = Agent(repo_root='.', agents_only=False, max_files=10)
agent.run()
```python

## Configuration Options

- `repo_root`: Root directory of the repository

- `agents_only`: Process only files in scripts/agent directory

- `max_files`: Maximum number of files to process

## File Processing Flow

- Discover code files recursively

- For each file, create supporting documentation files

- Run iterative improvement loop until no changes are detected

- Commit and push changes to git

## Supporting Files Created

For each code file `{name}.py`, the agent creates:

- `{name}.description.md`: Documentation and context

- `{name}.changes.md`: Changelog

- `{name}.errors.md`: Error reports

- `{name}.improvements.md`: Improvement suggestions

- `{name}.tests.py`: Test suite

## Change Detection

The agent uses file content comparison to detect when improvements have stabilized, preventing
infinite loops while ensuring all possible improvements are applied.

## Git Integration

Automatically commits changes with descriptive messages and pushes to the remote repository.
