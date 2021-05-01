from datetime import date
from typing import Optional


class Task:
    description: str
    priority: Optional[str]
    completed: Optional[date]
    due: Optional[date]

    def __init__(self, line: str):
        words = line.split()
        self.completed = None
        if words[0] == "x":
            self.completed = date.fromisoformat(words[1])
            words = words[2:]
        self.priority = None
        if words[0].startswith("(") and words[0].endswith(")"):
            # Should require priority to be a single upper-case letter
            self.priority = words[0].removeprefix("(").removesuffix(")")
            words = words[1:]
        description_words = []
        self.due = None
        for word in words:
            if word.startswith("due:"):
                self.due = date.fromisoformat(word.removeprefix("due:"))
            else:
                description_words.append(word)
        self.description = " ".join(description_words)

    def complete(self):
        if not self.completed:
            self.completed = date.today()
            self.priority = None

    def __str__(self):
        words = []
        if self.completed:
            words.append("x")
            words.append(self.completed.isoformat())

        if self.priority is not None:
            words.append("(" + self.priority + ")")

        if self.due is not None:
            words.append("due:" + self.due.isoformat())

        words.append(self.description)
        return " ".join(words) + "\n"
