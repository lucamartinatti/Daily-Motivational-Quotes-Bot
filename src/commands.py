import os
import time

from typing import Final
from dotenv import load_dotenv
from datetime import time
from telegram import Update
from telegram.ext import (
    ContextTypes,
    CallbackContext,
    Application,
)

from src.logic import get_quote

load_dotenv()
CHAT_ID: Final = os.getenv("CHAT_ID")
BOT_USERNAME: Final = os.getenv("BOT_USERNAME")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hello! I am a bot that sends you daily motivational quotes."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "You can use the following commands:\n"
        "/start - Start the bot\n"
        "/help - Get help\n"
        "/quote - Get a motivational quote"
    )


async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    quote = get_quote()
    await update.message.reply_text(quote)


def handle_response(text: str) -> None:
    formatted_text = text.lower()
    if "quote" in formatted_text:
        return get_quote()
    else:
        return "I don't understand that command."


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_type = update.message.chat.type
    text = update.message.text

    print(
        f"User: {update.message.chat.id} - Received message: {text} - Message type: {message_type}"
    )

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, "").strip()
            response = handle_response(new_text)
        else:
            return
    else:
        response = handle_response(text)

    print(f"Bot response: {response}")

    await update.message.reply_text(response)


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"This update: {update} causes the following error: {context.error}")


### Scheduling messages ###
async def send_daily_quote(context: CallbackContext) -> None:
    print("Sending daily quote...")
    quote = get_quote()
    await context.bot.send_message(chat_id=CHAT_ID, text=quote)


# Function to schedule the daily quote job
def schedule_daily_quote(app: Application) -> None:
    """Schedule the daily quote job."""
    app.job_queue.run_daily(
        send_daily_quote,  # Function to send the quote
        days=(0, 1, 2, 3, 4, 5, 6),  # Run every day of the week (0=Monday, 6=Sunday)
        time=time(hour=6, minute=30),  # UTC time
    )
