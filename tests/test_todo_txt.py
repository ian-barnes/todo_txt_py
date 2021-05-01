from todo_txt.task import Task
from todo_txt import __version__


def test_version():
    assert __version__ == '0.1.0'

def test_list():
    pass

def test_complete():
    pass

def test_add():
    pass

def test_task_inout():
    line = "x 2021-04-12 Do this task\n"
    task = Task(line)
    assert str(task) == line
