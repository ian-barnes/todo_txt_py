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

    if cmd == "list":
        pass
    elif cmd == "complete":
        tasknum = int(sys.argv[2])
        tasks[tasknum].complete()
    elif cmd == "add":
        task = Task(" ".join(args))
        tasks.append(task)
    else:
        print(f"Unknown command {cmd}")

    list_tasks(tasks)

    # Now write the (possibly updated) list back to file
