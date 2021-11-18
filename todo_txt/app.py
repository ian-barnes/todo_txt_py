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

commands = {
    "list": ("list tasks", lambda args: list(args)),
    "complete": ("mark a task as complete", lambda args: complete(args)),
    "add": ("add a new task", lambda args: add(args)),
    "prioritise": ("prioritise a task", lambda args: prioritise(args)),
    "deprioritise": ("deprioritise a task", lambda args: deprioritise(args)),
    "delete": ("delete a task", lambda args: delete(args)),
    "report": ("print task statistics", lambda args: report(args)),
    "help": ("list commands", lambda args: help(args)),
}


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


def list(args: List[str]):
    tasks = read_tasks_from_file()
    list_tasks(tasks)


def complete(args: List[str]):
    tasknum = int(args[0])
    tasks = read_tasks_from_file()
    tasks[tasknum].complete()
    write_tasks_to_file(tasks)


def add(words: List[str]):
    tasks = read_tasks_from_file()
    task = Task(" ".join(words))
    tasks.append(task)
    write_tasks_to_file(tasks)


def prioritise(args: List[str]):
    tasknum = int(args[0])
    priority = args[1]
    tasks = read_tasks_from_file()
    priority = priority[0].upper()
    assert len(priority) == 1 and priority[0] in alphabet
    tasks[tasknum].set_priority(priority)
    write_tasks_to_file(tasks)


def deprioritise(args: List[str]):
    tasknum = int(args[0])
    tasks = read_tasks_from_file()
    tasks[tasknum].unset_priority()
    write_tasks_to_file(tasks)


def delete(args: List[str]):
    tasknum = int(args[0])
    tasks = read_tasks_from_file()
    del tasks[tasknum]
    write_tasks_to_file(tasks)


def report(args: List[str]):
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


def help(args: List[str]):
    for (name, value) in commands.items():
        (helptext, _) = value
        print(f"{name}: {helptext}")


def find_matching_commands(usercmd):
    matching = []
    for command in commands.keys():
        if command.startswith(usercmd):
            matching.append(command)
    return matching


def report_ambiguous(cmds):
    # todo: use strjoin
    sys.stderr.write("ambiguous command, it could be ")
    for i in range(len(cmds)):
        if i > 0:
            sys.stderr.write(" or ")
        sys.stderr.write(cmds[i])
    sys.stderr.write("\n")


def parse_cmd_line():
    if len(sys.argv) == 1:
        cmd = "help"
        args = None
    else:
        usercmd = sys.argv[1]
        args = sys.argv[2:]
        cmds = find_matching_commands(usercmd)
        if len(cmds) == 0:
            sys.stderr.write("no matching command\n")
            sys.exit(1)
        elif len(cmds) == 1:
            cmd = cmds[0]
        else:
            report_ambiguous(cmds)
            sys.exit(1)
    return (cmd, args)


def run():
    (cmd, args) = parse_cmd_line()
    (_, fn) = commands[cmd]
    fn(args)
