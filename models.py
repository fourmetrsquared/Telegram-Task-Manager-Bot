# Data models
import time


class Task:
    """Represents a task with name, day, time, and metadata"""

    def __init__(self, name, task_day="", task_time=""):
        self.id = time.time()
        self.name = name
        self.day = task_day
        self.time = task_time
        self.message_id = 0

    def __repr__(self):
        return f"Task('{self.name}', '{self.day}', '{self.time}')"

    def to_dict(self):
        """Convert Task object to dictionary for serialization"""
        return {
            "type": "Task",
            "id": self.id,
            "name": self.name,
            "day": self.day,
            "time": self.time,
            "message_id": self.message_id
        }

    @classmethod
    def from_dict(cls, data):
        """Create Task object from dictionary"""
        if data.get("type") == "Task":
            task = cls(
                name=data.get("name", ""),
                task_day=data.get("day", ""),
                task_time=data.get("time", "")
            )
            task.id = data.get("id", time.time())
            task.message_id = data.get("message_id", 0)
            return task
        return data