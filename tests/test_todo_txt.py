from todo_txt.task import Task


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
