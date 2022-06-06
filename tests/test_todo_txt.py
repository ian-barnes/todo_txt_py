import pytest
from click.testing import CliRunner

import todo_txt.app as app
from todo_txt.task import Task

todo_file = "todo.txt"


@pytest.fixture(autouse=True)
def setup_function(pytester: pytest.Pytester):
    # Prepare fresh todo.txt for each test
    pytester.copy_example(todo_file)


def test_list():
    runner = CliRunner()
    result = runner.invoke(app.list)

    assert result.exit_code == 0


def test_complete():
    pass


def test_add():
    pass


def test_task_inout():
    line = "x 2021-04-12 Do this task"
    task = Task(line)

    assert str(task) == line
