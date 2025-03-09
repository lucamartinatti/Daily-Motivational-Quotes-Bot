import os

from typing import Final
from dotenv import load_dotenv
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from src.commands import (
    start_command,
    help_command,
    quote_command,
    handle_message,
    handle_error,
    schedule_daily_quote,
)


load_dotenv()
TOKEN: Final = os.getenv("TOKEN")


def main():

    print("Start Bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("quote", quote_command))

    # Message
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error
    app.add_error_handler(handle_error)

    # Schedule daily quote
    schedule_daily_quote(app)

    # Run the bot
    print("Polling...")
    app.run_polling(poll_interval=2)


if __name__ == "__main__":
    main()
