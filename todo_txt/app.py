import sys
from os import remove
from shutil import copyfile
from typing import Dict, List

from .task import Task

todo_file = "todo.txt"
backup_file = "backup.txt"
error_file = "error.txt"
done_file = "done.txt"


def print_task_list(tasks: List[Task]):
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


def list_tasks(tasks: List[Task], args: List[str]):
    print_task_list(tasks)


def complete(tasks: List[Task], args: List[str]):
    tasknum = int(args[0])
    tasks[tasknum].complete()
    write_tasks_to_file(tasks)


def add(tasks: List[Task], words: List[str]):
    task = Task(" ".join(words))
    tasks.append(task)
    write_tasks_to_file(tasks)


def prioritise(tasks: List[Task], args: List[str]):
    tasknum = int(args[0])
    priority = args[1]
    if len(priority) == 1 and priority[0].isalpha():
        priority = priority[0].upper()
        try:
            tasks[tasknum].set_priority(priority)
            write_tasks_to_file(tasks)
        except Exception:
            print(f"Couldn't set priority on task {tasknum}")
    else:
        print("Priority must be a single letter")


def deprioritise(tasks: List[Task], args: List[str]):
    tasknum = int(args[0])
    tasks[tasknum].unset_priority()
    write_tasks_to_file(tasks)


def delete(tasks: List[Task], args: List[str]):
    tasknum = int(args[0])
    del tasks[tasknum]
    write_tasks_to_file(tasks)


def report(tasks: List[Task], args: List[str]):
    total = len(tasks)
    done = len([task for task in tasks if task.completed is not None])
    print(f"{total} tasks, {done} completed ({done * 100.0 / total:.1f}%)")
    priorities: Dict[str, int] = {}

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


def run():
    cmd = sys.argv[1]
    args = sys.argv[2:]

    cmd_actions = {
        "list": list_tasks,
        "complete": complete,
        "prioritise": prioritise,
        "deprioritise": deprioritise,
        "delete": delete,
        "report": report,
    }
    tasks = read_tasks_from_file()

    if cmd in cmd_actions:
        cmd_actions[cmd](tasks, args)
    else:
        # see how to handle autocomplete
        matched_cmd = []
        for k in cmd_actions.keys():
            if k.startswith(cmd):
                matched_cmd.append(k)
        if len(matched_cmd) == 0:
            print(f"Unknown command {cmd}")
        elif len(matched_cmd) == 1:
            allow_completion = input(f"Completing to command {matched_cmd[0]} [Y/N] ")
            if allow_completion.lower() == "y":
                cmd_actions[matched_cmd[0]](tasks, args)
        else:
            print("Possible matched: " + (", ".join(matched_cmd)))
