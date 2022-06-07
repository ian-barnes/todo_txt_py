from .ICommand import ICommand


class ListCommand(ICommand):
    def __init__(self, filter) -> None:
        super().__init__()
        self._filter = filter

    def Execute(self, task_list) -> str:
        ret = []
        for i, task in enumerate(task_list):
            for w in task:
                if self._filter.lower() in w.lower():
                    ret.append(f"[{i}]: {str(task)}")
                    break

        return ret
