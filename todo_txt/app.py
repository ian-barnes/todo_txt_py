import shutil
import sys
from typing import List

from .task import Task


def list_tasks(tasks: List[Task]):
    for i, item in enumerate(tasks):
        line = f"[{i}]:"
        if item.completed:
            line += f" completed: {item.completed.isoformat()}"
        if item.priority:
            line += f" priority: {item.priority}"
        line += f" description: {item.description}"
        print(line)


def run():
    cmd = sys.argv[1]
    args = sys.argv[2:]

    with open("todo.txt") as file:
        lines = file.readlines()
    tasks = [Task(line) for line in lines]

    changed = False

    if cmd == "list":
        pass
    elif cmd == "complete":
        tasknum = int(args[0])
        tasks[tasknum].complete()
        changed = True
    elif cmd == "add":
        task = Task(" ".join(args))
        tasks.append(task)
        changed = True
    else:
        print(f"Unknown command {cmd}")

    list_tasks(tasks)

    # Now write the (possibly updated) list back to file
    if changed:
        shutil.copyfile("todo.txt", "archive.txt")
        lines = [str(task) for task in tasks]
        try:
            with open("todo.txt", "w") as file:
                file.writelines(lines)
        except Exception:
            print("An error happened in file writing")
            shutil.copyfile("todo.txt", "error.txt")
            shutil.copyfile("archive.txt", "todo.txt")
