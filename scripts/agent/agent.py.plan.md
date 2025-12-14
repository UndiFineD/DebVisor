
# agent.py

use the other files in this folder as templates

## description

you are an agent assigning work to other agents,
this may or may not run async, depending on the task and previous condition has been met.

## starting flags

the default --dir option is . but user may specify a different directory to process

the default --loop=1

We have an option to run as --agents-only
where only the files in this scripts\agent directory are to be processed.

We have an option of --max-files
that limits the amount of files we will fix in a run limited to regardless of the amount of files
overal selected. for example --max-files=20 will only do the first 20 Codefile it sees in the
directory selected.

## file filtering

you are going to Select which files and directories are relevant
some directories and files may be excluded in `.codeignore`

The fixing process is in a loop until all is marked as fixed, or --loop=5 times the loop has been
traversed or the loop is willfully exited

```python
- Read the classes Context, Changelog, Errors, Improvements
- give a Stats update
- Run the Tests on the Codefile
- Update Errors, Improvements
- Update Code
- Update Changelog, Context, Tests
- git add -A , git commit, git push

```python

give a Stats update

## Context update

make a class that calls upon

make agent-context.py
that reads a specified --context Contextfile Codefile.description.md and returns this context into
previous-context

then the agent-context.py will wait for --prompt
runSubagent will improve a complete summary description of the CodeFile

and update context Contextfile into current-context

make a diff between current-context and previous-context

## Changelog update

make a class that calls upon

make agent-changes.py
that reads a specified --context file Codefile.changes.md and returns this context into
previous-context

then the agent-changes.py will wait for --prompt
and update context file into current-context

make a diff between current-context and previous-context

## Errors update

make a class that calls upon

make agent-errors.py
that reads a specified --context file Codefile.errors.md and returns this context into
previous-context

then the agent-errors.py will wait for --prompt
and update context file into current-context

make a diff between current-context and previous-context

## Improvements update

make a class that calls upon

make agent-improvements.py
that reads a specified --context file Codefile.improvements.md and returns this context into
previous-context

then the agent-improvements.py will wait for --prompt
and update context file into current-context

make a diff between current-context and previous-context

## Tests update

make a class that calls upon

make agent-tests.py
that reads a specified --context file Codefile.tests.py and returns this context into
previous-context

then the agent-tests.py will wait for --prompt
it can use standard tools, or create its own tests in python Codefile.tests.py , as long as each
line of Codefile is tested by at least one test

and update context file into current-context

make a diff between current-context and previous-context

## Code update

make a class that calls upon

make agent-coder.py
that reads a specified --context Codefile and returns this context into previous-context

then the agent-coder.py will wait for --prompt
and update context Codefile into current-context

make a diff between current-context and previous-context

## Stats update

make a class that informes us about
which file, how make updates are needed and how many are done
