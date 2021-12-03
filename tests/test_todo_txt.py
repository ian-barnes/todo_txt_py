from todo_txt.task import Task
from todo_txt.app import is_unique, does_pattern_matching, list_tasks

MOCK_TASKS = ["Call ian", "call antoine", "sleep well"]
EXPECTED = ["[0]: Call ian", "[1]: call antoine", "[2]: sleep well"]


def test_list():
    assert list_tasks(MOCK_TASKS) == "\n".join(EXPECTED)
    assert list_tasks(MOCK_TASKS, "Call") == "[0]: Call ian\n[1]: call antoine"
    assert list_tasks(MOCK_TASKS, "call") == "\n".join(EXPECTED[0:2])
    assert list_tasks(MOCK_TASKS, "") == "\n".join(EXPECTED)
    assert list_tasks(MOCK_TASKS, "eat vegetables") == ""
    assert list_tasks(MOCK_TASKS, "all") == "\n".join(EXPECTED[0:2])


def test_complete():
    pass


def test_add():
    pass


def test_task_inout():
    line = "x 2021-04-12 Do this task"
    task = Task(line)
    assert str(task) == line


def test_is_unique():
    assert is_unique("l")
    assert is_unique("d") is False
    assert is_unique("z")


def test_does_pattern_matching():
    assert does_pattern_matching("", "list") is False
    assert does_pattern_matching("l", "") is False
    assert does_pattern_matching("l", "list")
    assert does_pattern_matching("list", "list")
    assert does_pattern_matching("d", "delete")
    assert does_pattern_matching("d", "deprioritize")
    assert does_pattern_matching("bonjour", "test") is False
