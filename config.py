# Bot configuration settings
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN', 'your_default_bot_token_here')

# File paths
DATA_FILE = "data.json"

# Button labels
BUTTONS = ["New task ✏️", "To-do list 📋"]
WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
TASK_ACTIONS = ["✅", "❌", "🗓", "🕒"]

# Time settings
TIME_START = 7
TIME_END = 21

# Messages
WELCOME_MESSAGE = "Hello, what needs to be done? 🙃"
HELP_MESSAGE = """Hello! Here is a list of available commands:
/start - start working
/help - list of available commands
/new_task - add a new task
/todo_list - view to-do list"""
TASK_PROMPT = "✏️ Enter task name:"
EMPTY_LIST_MESSAGE = "Your list is empty! 😕"
TASK_ADDED_MESSAGE = "✏️ Task added \n{task_name}"
TASK_COMPLETED_MESSAGE = "Task completed ✅"
TASK_DELETED_MESSAGE = "Task deleted ❌"
TASK_FORMAT = "🔸 Task № {task_number}. {task_name}\n{task_day} {task_time}"