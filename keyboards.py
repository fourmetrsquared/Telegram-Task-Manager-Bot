# Keyboard generators
from telebot import types
import json
from config import WEEK_DAYS, TASK_ACTIONS, TIME_START, TIME_END


class KeyboardFactory:
    """Factory for creating different types of keyboards"""

    @staticmethod
    def create_main_keyboard():
        """Create the main reply keyboard"""
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
        )
        new_task_btn = types.KeyboardButton("New task ✏️")
        todo_list_btn = types.KeyboardButton("To-do list 📋")
        markup.row(new_task_btn, todo_list_btn)
        return markup

    @staticmethod
    def create_task_keyboard(task_id: float):
        """Create inline keyboard for task actions"""
        keyboard = types.InlineKeyboardMarkup(row_width=4)
        keyboard_buttons = []

        for action in TASK_ACTIONS:
            data = {'id': task_id, 'action': action}
            json_string = json.dumps(data)
            button = types.InlineKeyboardButton(action, callback_data=json_string)
            keyboard_buttons.append(button)

        keyboard.add(*keyboard_buttons)
        return keyboard

    @staticmethod
    def create_day_keyboard(task_id: float):
        """Create inline keyboard for day selection"""
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard_buttons = []

        for day in WEEK_DAYS:
            data = {'id': task_id, 'action': 'day', 'day_index': WEEK_DAYS.index(day)}
            json_string = json.dumps(data)
            button = types.InlineKeyboardButton(day, callback_data=json_string)
            keyboard_buttons.append(button)

        keyboard.add(*keyboard_buttons)
        return keyboard

    @staticmethod
    def create_time_keyboard(task_id: float):
        """Create inline keyboard for time selection"""
        keyboard = types.InlineKeyboardMarkup(row_width=5)
        keyboard_buttons = []

        for hour in range(TIME_START, TIME_END + 1):
            time_str = f"{hour}:00"
            data = {'id': task_id, 'action': 'time', 'time': time_str}
            json_string = json.dumps(data)
            button = types.InlineKeyboardButton(time_str, callback_data=json_string)
            keyboard_buttons.append(button)

        keyboard.add(*keyboard_buttons)
        return keyboard