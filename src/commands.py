from datetime import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CallbackContext,
    ContextTypes,
    ConversationHandler,
)

from src.constants import MENU, OPTION1, OPTION2, OPTION3, OPTION4, OPTION5
from src.logic import get_quote, quote_for_specific_user
from src.db_tools import (
    get_scheduled_chat,
    insert_user_data,
)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    insert_user_data(update.message.chat)
    keyboard = [
        [InlineKeyboardButton("Motivation", callback_data="motivation")],
        [InlineKeyboardButton("Philosophy", callback_data="philosophy")],
        [InlineKeyboardButton("Stoic", callback_data="stoic")],
        [InlineKeyboardButton("Life", callback_data="life")],
        [InlineKeyboardButton("Love", callback_data="love")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hello! I am a bot that sends you daily motivational quotes.",
        reply_markup=reply_markup,
    )
    return MENU


async def button(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "motivation":
        await query.edit_message_text(text="You will Motivational quotes.")
        return OPTION1
    elif query.data == "philosophy":
        await query.edit_message_text(text="You will receive Philosophical quotes.")
        return OPTION2
    elif query.data == "stoic":
        await query.edit_message_text(text="You will receive Stoic quotes.")
        return OPTION3
    elif query.data == "life":
        await query.edit_message_text(text="You will receive Life related quotes.")
        return OPTION4
    elif query.data == "love":
        await query.edit_message_text(text="You will receive Love related quotes.")
        return OPTION5
    else:
        await query.edit_message_text(text="Unknown option selected.")
        return MENU


async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "You can use the following commands:\n"
        "/start - Start the bot or select a new category\n"
        "/help - Get help\n"
        "/quote - Get a motivational quote"
    )


async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    quote = quote_for_specific_user(update.message.chat.id)
    await update.message.reply_text(quote)


# Scheduling messages
async def send_daily_quote(context: CallbackContext) -> None:
    print("Sending daily quote...")
    quote = get_quote(context.job.data[1])
    await context.bot.send_message(chat_id=context.job.data[0], text=quote)


# Function to schedule the daily quote job
def schedule_daily_quote(app: Application) -> None:
    """Schedule the daily quote job."""
    for user_data in get_scheduled_chat():
        app.job_queue.run_daily(
            send_daily_quote,  # Function to send the quote
            data=user_data,  # Data to pass to the function
            days=(
                0,
                1,
                2,
                3,
                4,
                5,
                6,
            ),  # Run every day of the week (0=Monday, 6=Sunday)
            time=time(hour=6, minute=30),  # UTC time
        )
