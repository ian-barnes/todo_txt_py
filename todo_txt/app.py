from os import remove
from shutil import copyfile
from typing import List

import click

from .task import Task

todo_file = "todo.txt"
backup_file = "backup.txt"
error_file = "error.txt"
done_file = "done.txt"


def list_tasks(tasks: List[Task]):
    for i, item in enumerate(tasks):
        print(f"[{i}]: {str(item)}")


def read_tasks_from_file() -> List[Task]:
    with open(todo_file, "r") as file:
        lines = file.readlines()
    return [Task(line) for line in lines]


def write_tasks_to_file(tasks: List[Task]):
    copyfile(todo_file, backup_file)
    lines = "\n".join(str(task) for task in tasks)
    try:
        with open(todo_file, "w") as file:
            file.write(lines + "\n")
    except Exception:
        print("An error happened in file writing")
        copyfile(todo_file, error_file)
        copyfile(backup_file, todo_file)
    finally:
        remove(backup_file)


@click.group()
def cli():
    """todo.txt in Python"""


@cli.command()
def list():
    """List all tasks"""
    tasks = read_tasks_from_file()
    for i, item in enumerate(tasks):
        print(f"[{i}]: {str(item)}")


@cli.command()
@click.argument("tasknum", type=click.INT, required=True)
# @click.option("--when", click.DATE, default=now())  # DATE type doesn't exist
def complete(tasknum: int):
    """Mark task TASKNUM as completed"""
    tasks = read_tasks_from_file()
    tasks[tasknum].complete()
    write_tasks_to_file(tasks)


@cli.command()
@click.argument("words", type=click.STRING, nargs=-1, required=True)
def add(words: List[str]):
    """Add a new task to the list"""
    tasks = read_tasks_from_file()
    task = Task(" ".join(words))
    tasks.append(task)
    write_tasks_to_file(tasks)


def uppercase_first_char(s: str) -> str:
    return s.upper()[0]


@cli.command()
@click.argument("tasknum", type=click.INT, required=True)
@click.argument("priority", type=click.STRING, required=True)
def prioritise(tasknum: int, priority: str):
    """Set the priority for task TASKNUM to PRIORITY ('A'...'Z')"""
    tasks = read_tasks_from_file()
    priority = uppercase_first_char(priority)
    assert len(priority) == 1 and priority[0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    tasks[tasknum].set_priority(priority)
    write_tasks_to_file(tasks)


@cli.command()
@click.argument("tasknum", type=click.INT, required=True)
def deprioritise(tasknum: int):
    """Remove any priority from task TASKNUM"""
    tasks = read_tasks_from_file()
    tasks[tasknum].unset_priority()
    write_tasks_to_file(tasks)
