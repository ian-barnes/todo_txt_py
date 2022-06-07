import pytest
from click.testing import CliRunner

import todo_txt.app as app
from todo_txt.Commands.ListCommand import ListCommand
from todo_txt.task import Task

todo_file = "todo.txt"


@pytest.fixture(autouse=True)
def setup_function(pytester: pytest.Pytester):
    # Prepare fresh todo.txt for each test
    pytester.copy_example(todo_file)


LIST_TASK = [Task("Tache 1 ach"), Task("Tache 2")]


def test_list_case_sensitive():

    list_command_lower = ListCommand("Tache")
    list_command_upper = ListCommand("tache")

    assert list_command_lower.Execute(LIST_TASK) == list_command_upper.Execute(
        LIST_TASK
    )


def test_filtered_list():

    list_command_one = ListCommand("2")
    list_command_zero = ListCommand("3")

    result = list_command_one.Execute(LIST_TASK)
    assert len(result) == 1
    assert result[0] == f"[1]: {str(LIST_TASK[1])}"

    result = list_command_zero.Execute(LIST_TASK)
    assert len(result) == 0


def test_list():
    runner = CliRunner()
    result = runner.invoke(app.list)
    assert result.exit_code == 0

    list_command = ListCommand("")
    i = 0
    for line in list_command.Execute(LIST_TASK):
        assert line == f"[{i}]: {str(LIST_TASK[i])}"
        i += 1

    list_command = ListCommand("ach")
    i = 0
    for line in list_command.Execute(LIST_TASK):
        assert line == f"[{i}]: {str(LIST_TASK[i])}"
        i += 1


def test_complete():
    pass


def test_add():
    pass


def test_task_inout():
    line = "x 2021-04-12 Do this task"
    task = Task(line)

    assert str(task) == line
