# todo_txt_py

Minimal toy [todo.txt][todo-txt-github] implementation in Python.

## Install

Set up a virtual environment if you want, however you usually do it. (One
possible way described below.)

Run `poetry install`.

## Usage

To run:

```bash
todo <cmd> <args>
```

## Development

To format code, check linting, run tests etc., use the `Makefile`. Just running
`make` will list the targets.

## Purpose

This is not intended as a production project, but mostly as a source of easy
exercises for pair programming interviews and as a sandbox for learning more
about project setup, structure, packaging, CI and so on.

As such, it comes with absolutely no guarantee that it does anything useful or
correct at all. It should not be used other than to play with.

## To do

In the spirit of [eating your own dog food][dog-food], the project to do list is
stored in the top-level `todo.txt`. To view it, run `todo list`.

## Notes

- I'm aware that class `Task` and its constructor could be simplified using
  `attrs`, but I didn't want to require too much Python knowledge to be able to
  work on this.
- In some ways this is deliberately a bit sloppy so as to generate opportunities
  for discussion and criticism.

## Useful links

- [todo.txt format][todo-txt-format]
- [Reference CLI usage/spec][todo-txt-cli]
- [Dropbox Python API  Docs][dropbox-api]
- [Google Drive Python API Quickstart][google-drive-api]

## Example virtual environment setup

Just one possible example of how to set things up for development, not
necessarily optimal:

Poetry sets up a virtual environment and [direnv][direnv] automates
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

[direnv]: https://direnv.net/
[dog-food]: https://en.wikipedia.org/wiki/Eating_your_own_dog_food
[todo-txt-github]: https://github.com/todotxt
[todo-txt-format]: https://github.com/todotxt/todo.txt
[todo-txt-cli]: https://github.com/todotxt/todo.txt-cli
[dropbox-api]: https://www.dropbox.com/developers/documentation/python
[google-drive-api]: https://developers.google.com/drive/api/v3/quickstart/python
