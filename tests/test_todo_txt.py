from todo_txt.task import Task
from todo_txt.app import is_unique, does_pattern_matching

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

def test_is_unique():
    assert is_unique('l')
    assert is_unique('d') is False
    assert is_unique('z')

def test_does_pattern_matching():
    assert does_pattern_matching('', 'list') is False
    assert does_pattern_matching('l', '') is False
    assert does_pattern_matching('l', 'list')
    assert does_pattern_matching('list', 'list')
    assert does_pattern_matching('d', 'delete')
    assert does_pattern_matching('d', 'deprioritize')
    assert does_pattern_matching('bonjour', 'test') is False