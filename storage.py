# Data storage management
import json
import os
from typing import Dict, List, Any
from models import Task


class StorageManager:
    """Manages reading and writing task data to JSON file"""

    def __init__(self, filename="data.json"):
        self.filename = filename
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """Create data file if it doesn't exist"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                json.dump({}, file)

    def read_all_data(self) -> Dict[str, List[Task]]:
        """Read all task data from file"""
        if os.path.getsize(self.filename) == 0:
            return {}

        try:
            with open(self.filename, 'r') as file:
                data = json.load(file, object_hook=Task.from_dict)
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def write_all_data(self, data: Dict[str, List[Task]]):
        """Write all task data to file"""
        try:
            with open(self.filename, 'w') as file:
                json.dump(data, file, default=self._serialize_task, indent=2)
        except IOError as e:
            print(f"Error writing to file: {e}")

    def _serialize_task(self, obj):
        """Custom serializer for Task objects"""
        if isinstance(obj, Task):
            return obj.to_dict()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    def get_user_tasks(self, chat_id: str) -> List[Task]:
        """Get tasks for a specific user"""
        all_data = self.read_all_data()
        return all_data.get(str(chat_id), [])

    def save_user_tasks(self, chat_id: str, tasks: List[Task]):
        """Save tasks for a specific user"""
        all_data = self.read_all_data()
        all_data[str(chat_id)] = tasks
        self.write_all_data(all_data)