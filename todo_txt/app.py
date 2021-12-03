import sys
from os import remove
from shutil import copyfile
from typing import List

from .task import Task

todo_file = "todo.txt"
backup_file = "backup.txt"
error_file = "error.txt"
done_file = "done.txt"

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


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


def list():
    tasks = read_tasks_from_file()
    list_tasks(tasks)


def complete(tasknum: int):
    tasks = read_tasks_from_file()
    tasks[tasknum].complete()
    write_tasks_to_file(tasks)


def add(words: List[str]):
    tasks = read_tasks_from_file()
    task = Task(" ".join(words))
    tasks.append(task)
    write_tasks_to_file(tasks)


def prioritise(tasknum: int, priority: str):
    tasks = read_tasks_from_file()
    priority = priority[0].upper()
    assert len(priority) == 1 and priority[0] in alphabet
    tasks[tasknum].set_priority(priority)
    write_tasks_to_file(tasks)


def deprioritise(tasknum: int):
    tasks = read_tasks_from_file()
    tasks[tasknum].unset_priority()
    write_tasks_to_file(tasks)


def delete(tasknum: int):
    tasks = read_tasks_from_file()
    del tasks[tasknum]
    write_tasks_to_file(tasks)


def report():
    tasks = read_tasks_from_file()
    total = len(tasks)
    done = len([task for task in tasks if task.completed is not None])
    print(f"{total} tasks, {done} completed ({done * 100.0 / total:.1f}%)")
    priorities = {}
    for task in tasks:
        p = task.priority
        if p is not None:
            if p in priorities:
                priorities[p] += 1
            else:
                priorities[p] = 1
    if priorities != {}:
        print("Task counts by priority:")
        for (priority, count) in sorted(priorities.items()):
            print(f"({priority}) -> {count}")

AVAILABLE_CMDS = ["list", "complete", "add", "prioritise", "deprioritise", "delete", "report"]
def does_pattern_matching(pattern: str, name: str) -> bool:
    return bool(pattern) and name.startswith(pattern)

def is_unique(pattern: str) -> bool:
    return [cmd.startswith(pattern) for cmd in AVAILABLE_CMDS].count(True) <= 1

def run():
    cmd = sys.argv[1]
    args = sys.argv[2:]

    if not is_unique(cmd):
        print("More than one cmd available")
        return

    if does_pattern_matching(cmd,"list"):
        list()
    elif does_pattern_matching(cmd,"complete"):
        tasknum = int(args[0])
        complete(tasknum)
    elif does_pattern_matching(cmd,"add"):
        add(args)
    elif does_pattern_matching(cmd,"prioritise"):
        tasknum = int(args[0])
        priority = args[1]
        prioritise(tasknum, priority)
    elif does_pattern_matching(cmd,"deprioritise"):
        tasknum = int(args[0])
        deprioritise(tasknum)
    elif does_pattern_matching(cmd,"delete"):
        tasknum = int(args[0])
        delete(tasknum)
    elif does_pattern_matching(cmd,"report"):
        report()
    else:
        print(f"Unknown command {cmd}")
