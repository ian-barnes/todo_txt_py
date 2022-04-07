import sys
from os import remove
from shutil import copyfile
from typing import List
from re import match, search

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


def list(**kwargs):
    tasks = read_tasks_from_file()
    list_tasks(tasks)

def complete(**kwargs):
    try:
        tasknum = kwargs["tasknum"]
    except KeyError:
        print("Usage: todo complete <tasknum>")
    tasknum = int(tasknum)
    tasks = read_tasks_from_file()
    tasks[tasknum].complete()
    write_tasks_to_file(tasks)


def add(**kwargs):
    try:
        words = kwargs["words"]
    except KeyError:
        print("Usage: todo add <words>")

    tasks = read_tasks_from_file()
    task = Task(" ".join(words))
    tasks.append(task)
    write_tasks_to_file(tasks)


def prioritise(**kwargs):
    try:
        tasknum = kwargs["tasknum"]
        priority = kwargs["priority"]
    except KeyError:
        print("Usage: todo prioritise <tasknum> <priority>")
    tasknum = int(tasknum)
    tasks = read_tasks_from_file()
    priority = priority[0].upper()
    assert len(priority) == 1 and priority[0] in alphabet
    tasks[tasknum].set_priority(priority)
    write_tasks_to_file(tasks)


def deprioritise(**kwargs):
    try:
        tasknum = kwargs["tasknum"]
    except KeyError:
        print("Usage: todo deprioritise <tasknum>")
    tasknum = int(tasknum)
    tasks = read_tasks_from_file()
    tasks[tasknum].unset_priority()
    write_tasks_to_file(tasks)


def delete(**kwargs):
    try:
        tasknum = kwargs["tasknum"]
    except KeyError:
        print("Usage: todo delete <tasknum>")
    tasknum = int(tasknum)
    tasks = read_tasks_from_file()
    del tasks[tasknum]
    write_tasks_to_file(tasks)


def report(**kwargs):
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


CMDS = {
    "list": list,
    "complete": complete,
    "add": add,
    "prioritise": prioritise,
    "deprioritise": deprioritise,
    "delete": delete,
    "report": report
}


def check_cmd(cmd: str) -> tuple[bool, List[str]]:

    args_ok = False

    matches = [CMDS[iter_cmd] for iter_cmd in CMDS.keys() if iter_cmd.startswith(cmd)]

    return args_ok, matches


def run_with_args(argv) -> List[str]:
    
    args_ok, matches = check_cmd(argv[1])

    if args_ok:
        cmd = argv[1]
        args = argv[2:]

        kwargs = {
            "tasknum": args[0] if len(args) > 0 else None,
            "priority": args[1] if len(args) > 1 else None,
            "words": args
        }

        # perform command
        matches[0](**kwargs)


    return matches

    # if cmd == "list":
    #     list()
    # elif cmd == "complete":
    #     tasknum = int(args[0])
    #     complete(tasknum)
    # elif cmd == "add":
    #     add(args)
    # elif cmd == "prioritise":
    #     tasknum = int(args[0])
    #     priority = args[1]
    #     prioritise(tasknum, priority)
    # elif cmd == "deprioritise":
    #     tasknum = int(args[0])
    #     deprioritise(tasknum)
    # elif cmd == "delete":
    #     tasknum = int(args[0])
    #     delete(tasknum)
    # elif cmd == "report":
    #     report()
    # else:
    #     print(f"Unknown command {cmd}")

def run():
    run_with_args(sys.argv)