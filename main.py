# Main bot implementation
import telebot
from telebot import types
import json

from config import *
from models import Task
from storage import StorageManager
from keyboards import KeyboardFactory

# Initialize bot and storage
bot = telebot.TeleBot(BOT_TOKEN)
storage = StorageManager(DATA_FILE)


def get_user_tasks(chat_id):
    """Get tasks for a user and all data"""
    tasks = storage.get_user_tasks(chat_id)
    return tasks, storage.read_all_data()


def save_user_tasks(chat_id, tasks, all_data):
    """Save tasks for a user"""
    all_data[str(chat_id)] = tasks
    storage.write_all_data(all_data)


@bot.message_handler(commands=['start'])
def start_command(message):
    """Handle /start command"""
    markup = KeyboardFactory.create_main_keyboard()
    bot.send_message(message.chat.id, WELCOME_MESSAGE, reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_command(message):
    """Handle /help command"""
    bot.send_message(message.chat.id, HELP_MESSAGE)


@bot.message_handler(commands=['newtask'])
def new_task_command(message):
    """Handle /newtask command"""
    prompt_for_task_name(message)


@bot.message_handler(commands=['todolist'])
def todo_list_command(message):
    """Handle /todolist command"""
    display_todo_list(message)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    """Handle text messages"""
    if message.text == BUTTONS[0]:  # New task
        prompt_for_task_name(message)
    elif message.text == BUTTONS[1]:  # To-do list
        display_todo_list(message)
    else:
        # Assume any other text is a new task
        create_new_task(message)


def prompt_for_task_name(message):
    """Ask user for task name"""
    bot.send_message(message.chat.id, TASK_PROMPT)


def display_todo_list(message):
    """Display the user's to-do list"""
    tasks, all_data = get_user_tasks(message.chat.id)

    if not tasks:
        bot.send_message(message.chat.id, EMPTY_LIST_MESSAGE)
        return

    # Update all task messages
    for i, task in enumerate(tasks):
        try:
            bot.delete_message(message.chat.id, task.message_id)
        except:
            pass  # Message might not exist anymore

        task_text = TASK_FORMAT.format(
            task_number=i + 1,
            task_name=task.name,
            task_day=task.day,
            task_time=task.time
        )

        new_message = bot.send_message(
            message.chat.id,
            task_text,
            reply_markup=KeyboardFactory.create_task_keyboard(task.id)
        )

        task.message_id = new_message.id
        save_user_tasks(message.chat.id, tasks, all_data)


def create_new_task(message):
    """Create a new task from message text"""
    tasks, all_data = get_user_tasks(message.chat.id)
    new_task = Task(message.text)
    tasks.append(new_task)

    confirmation = bot.send_message(
        message.chat.id,
        TASK_ADDED_MESSAGE.format(task_name=new_task.name),
        reply_markup=KeyboardFactory.create_task_keyboard(new_task.id)
    )

    new_task.message_id = confirmation.id
    save_user_tasks(message.chat.id, tasks, all_data)


def update_task_day(call, task_id, day_index):
    """Update the day for a task"""
    tasks, all_data = get_user_tasks(call.message.chat.id)

    for i, task in enumerate(tasks):
        if task.id == task_id:
            task.day = WEEK_DAYS[day_index]
            save_user_tasks(call.message.chat.id, tasks, all_data)

            updated_text = TASK_FORMAT.format(
                task_number=i + 1,
                task_name=task.name,
                task_day=task.day,
                task_time=task.time
            )

            bot.edit_message_text(
                updated_text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=KeyboardFactory.create_task_keyboard(task.id)
            )
            bot.answer_callback_query(call.id)
            break


def update_task_time(call, task_id, time_str):
    """Update the time for a task"""
    tasks, all_data = get_user_tasks(call.message.chat.id)

    for i, task in enumerate(tasks):
        if task.id == task_id:
            task.time = time_str
            save_user_tasks(call.message.chat.id, tasks, all_data)

            updated_text = TASK_FORMAT.format(
                task_number=i + 1,
                task_name=task.name,
                task_day=task.day,
                task_time=task.time
            )

            bot.edit_message_text(
                updated_text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=KeyboardFactory.create_task_keyboard(task.id)
            )
            bot.answer_callback_query(call.id)
            break


def remove_task(call, task_id, message_text):
    """Remove a task from the list"""
    tasks, all_data = get_user_tasks(call.message.chat.id)

    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            save_user_tasks(call.message.chat.id, tasks, all_data)

            bot.edit_message_text(
                message_text,
                call.message.chat.id,
                call.message.message_id
            )
            bot.answer_callback_query(call.id)
            break


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    """Handle inline keyboard callbacks"""
    try:
        data = json.loads(call.data)
        task_id = data.get("id")
        action = data.get("action")

        if action == TASK_ACTIONS[0]:  # ✅ Complete task
            remove_task(call, task_id, TASK_COMPLETED_MESSAGE)
        elif action == TASK_ACTIONS[1]:  # ❌ Delete task
            remove_task(call, task_id, TASK_DELETED_MESSAGE)
        elif action == TASK_ACTIONS[2]:  # 🗓️ Set day
            bot.edit_message_text(
                call.message.text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=KeyboardFactory.create_day_keyboard(task_id)
            )
        elif action == 'day':
            day_index = data.get("day_index")
            update_task_day(call, task_id, day_index)
        elif action == TASK_ACTIONS[3]:  # 🕒 Set time
            bot.edit_message_text(
                call.message.text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=KeyboardFactory.create_time_keyboard(task_id)
            )
        elif action == 'time':
            time_str = data.get("time")
            update_task_time(call, task_id, time_str)

    except json.JSONDecodeError:
        bot.answer_callback_query(call.id, "Error processing request")
    except Exception as e:
        print(f"Error in callback handler: {e}")
        bot.answer_callback_query(call.id, "An error occurred")


if __name__ == "__main__":
    print("Bot is starting...")
    bot.polling(none_stop=True, interval=0)