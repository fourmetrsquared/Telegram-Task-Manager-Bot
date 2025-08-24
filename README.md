# Telegram Task Manager Bot
A sophisticated Telegram bot for task management built with Python and the pyTelegramBotAPI library. This production-ready solution features a clean architecture, persistent JSON storage, and an intuitive interface for managing tasks with day and time scheduling.

## 🚀 Features

- Task Management: Create, view, complete, and delete tasks
- Smart Scheduling: Assign tasks to specific days and times
- Interactive UI: Inline keyboards for seamless task management
- Multi-user Support: Isolated task lists for different users
- Data Persistence: JSON-based storage with proper serialization
- Responsive Design: Intuitive interface with visual feedback
## 🛠️ Tech Stack

- **Backend:** Python 3.8+
- **Telegram API:** pyTelegramBotAPI
- **Data Storage:** JSON with custom serialization
- **Architecture:** Modular class-based design
## 📦 Installation

1. Clone the repository:
  ```bash
  git clone https://github.com/yourusername/telegram-task-bot.git
  cd telegram-task-bot
  ```
2. Create a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```
3. Install dependencies:
  ```bash
  pip install pyTelegramBotAPI
  Configure your bot token:
  ```
  ```python
  # Replace with your actual bot token from @BotFather
  BOT_TOKEN = 'your_actual_bot_token_here'
```
4. Run the bot:
  ```bash
  python bot.py
  ```
## 🏗️ Project Structure

```text
telegram-task-bot/
├── main.py                 # Main bot implementation
├── config.py              # Configuration settings
├── models.py              # Data models (Task class)
├── storage.py             # JSON storage management
├── keyboards.py           # Inline keyboard generators
├── requirements.txt       # Project dependencies
├── data.json              # Task data (auto-generated)
└── README.md              # Project documentation
```
## 💡 Usage

1. Start a chat with your bot on Telegram
2. Use /start to initialize the bot
3. Create new tasks with "New task ✏️"
4. View your task list with "To-do list 📋"
5. Manage tasks using interactive buttons:
  - ✅ Mark as complete
  - ❌ Delete task
  - 🗓️ Assign to a day
  - 🕒 Set a time
  - 🔧 API Reference

## 🤖 Bot Commands

  - /start - Initialize the bot
  - /help - Show help information
  - /newtask - Create a new task
  - /todolist - Display current tasks
## 📋 Task Object

```python
class Task:
    def __init__(self, name, task_day="", task_time=""):
        self.id = time.time()  # Unique identifier
        self.name = name       # Task description
        self.day = task_day    # Scheduled day
        self.time = task_time  # Scheduled time
        self.message_id = 0    # Telegram message ID
```
## 🧪 Testing

Run the bot in development mode:

```bash
python bot.py
```
Test specific features by interacting with the bot through Telegram.

## 📈 Performance Notes

  - Uses efficient JSON serialization/deserialization
  - Implements proper error handling for file operations
  - Optimized keyboard generation with inline buttons
  - Memory-efficient task management
## 🔒 Security Considerations

  - Replace the example bot token with your actual token
  - Validate all user inputs
  - Implement rate limiting if necessary
  - Regularly backup the data.json file
## 🤝 Contributing

  - Fork the repository
  - Create a feature branch (git checkout -b feature/amazing-feature)
  - Commit your changes (git commit -m 'Add amazing feature')
  - Push to the branch (git push origin feature/amazing-feature)
  - Open a Pull Request
## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

🏆 Credits

Developed with fourmetrsquared❤️ using the pyTelegramBotAPI library.
