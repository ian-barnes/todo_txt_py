from todo_txt.task import Task
from todo_txt.app import check_cmd

import pytest

def test_list():
    pass

def test_complete():
    pass

def test_add():
    pass

def test_task_inout():
    line = "x 2021-04-12 Do this task"
    task = Task(line)
    assert str(task) == line

@pytest.mark.parametrize("cmd, count",[
        ("dep", 1),
        ("de", 2),
        ("z", 0),
])
def test_check_cmd(cmd, count):
    _, matches = check_cmd(cmd)
    assert len(matches) == count
