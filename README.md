# todo_txt_py

Minimal toy [todo.txt](https://github.com/todotxt) implementation in Python.

## Install

Set up a virtual environment if you want, however you usually do it. (One
possible way described below.)

Run `poetry install`.

## Usage

To run:

```bash
python -m todo_txt <cmd> <args>
```

or just

```bash
todo.sh <cmd> <args>
```

To format code, check linting, run tests etc., use the `Makefile`. Just running
`make` will list the targets.

## Purpose

This is not intended as a production project, but as a source of easy
exercises for pair programming interviews.

As such, it comes with absolutely no guarantee that it does anything useful or
correct at all. It should not be used other than to play with.

## Still to do

- Modularisation
- Meaningful unit tests
- Save modified todo list back to file
- Implement the following commands:
  - `delete`
  - `update` (called `replace` in the standard `todo.txt` CLI)
  - `prioritise`
  - `deprioritise`
  - `report`
  - `help` / `shorthelp`
- Everything relating to contexts and projects
- Sorting and filtering of the task list
- Multiple files? (not really necessary, apart from `done.txt` because it's in
  the standard)
- Some sort of config file and/or environment variable telling it where to find
  the file
- Syncing with Google Drive and/or Dropbox?
- An interactive mode with prompt and main loop
- Setting things up a bit more like a "normal" Python project, so that this is
  not dependent on being inside a virtual environment and so that it's also a
  re-usable package
- Allow unambiguous abbreviations of commands

## Notes

- I'm aware that class `Task` and its constructor could be simplified using
  `attrs`, but I didn't want to require too much Python knowledge to be able to
  work on this.
- In some ways this is all deliberately sloppy so as to generate opportunities
  for discussion and criticism.

## Useful links

- [todo.txt format](https://github.com/todotxt/todo.txt)
- [Reference CLI usage/spec](https://github.com/todotxt/todo.txt)
- [Dropbox Python API
  Docs](https://www.dropbox.com/developers/documentation/python)
- [Google Drive Python API
  Quickstart](https://developers.google.com/drive/api/v3/quickstart/python)

## Example virtual environment setup

Just one possible example of how to set things up for development, not
necessarily optimal:

Poetry sets up a virtual environment and [direnv](https://direnv.net/) automates
activating it whenever I go into the project directory.

I added the following snippet to my `.direnvrc`:

```bash
layout_poetry() {
  if [[ ! -f pyproject.toml ]]; then
    log_error 'No pyproject.toml found.  Use `poetry new` or `poetry init` to create one first.'
    exit 2
  fi

  local VENV=$(dirname $(poetry run which python))
  export VIRTUAL_ENV=$(echo "$VENV" | rev | cut -d'/' -f2- | rev)
  export POETRY_ACTIVE=1
  PATH_add "$VENV"
}
```

and then put this in the local `.envrc`:

```bash
layout poetry
```

Without doing the `direnv`, you can activate the virtual environment with
`poetry shell`.
