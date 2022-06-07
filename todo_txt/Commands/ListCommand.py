from .ICommand import ICommand 

class ListCommand(ICommand):
    def __init__(self, filter) -> None:
        super().__init__()
        self._filter = filter

    def Execute(self, task_list) -> str :
        ret = ""
        for i, item in enumerate(task_list):
            for w in item:           
                if self._filter.lower() in w.lower():
                    ret += f"[{i}]: {str(item)}\n"
        return ret[:- 1]
    
