from datetime import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CallbackContext,
    ContextTypes,
    ConversationHandler,
)

from src.constants import MENU, OPTION1, OPTION2, OPTION3, OPTION4, OPTION5, OPTION6
from src.logic import get_quote, quote_for_specific_user
from src.db_tools import (
    fetch_scheduled_chats,
    insert_user_data,
    update_user_category,
)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    insert_user_data(update.message.chat)
    keyboard = [
        [InlineKeyboardButton("Motivation", callback_data="motivation")],
        [InlineKeyboardButton("Philosophy", callback_data="philosophy")],
        [InlineKeyboardButton("Stoic", callback_data="stoic")],
        [InlineKeyboardButton("Life", callback_data="life")],
        [InlineKeyboardButton("Love", callback_data="love")],
        [InlineKeyboardButton("All", callback_data="all")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hello! Which category interests you most?",
        reply_markup=reply_markup,
    )
    return MENU


async def button(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    option = MENU
    if query.data == "motivation":
        await query.edit_message_text(
            text="You will receive motivational quotes on a daily basis."
        )
        option = OPTION1
    elif query.data == "philosophy":
        await query.edit_message_text(
            text="You will receive philosophical quotes on a daily basis."
        )
        option = OPTION2
    elif query.data == "stoic":
        await query.edit_message_text(
            text="You will receive stoic quotes on a daily basis."
        )
        option = OPTION3
    elif query.data == "life":
        await query.edit_message_text(
            text="You will receive life related quote on a daily basis."
        )
        option = OPTION4
    elif query.data == "love":
        await query.edit_message_text(
            text="You will receive love related quote on a daily basis."
        )
        option = OPTION5
    elif query.data == "all":
        await query.edit_message_text(
            text="You will receive quotes from all categories on a daily basis."
        )
        option = OPTION6
    else:
        await query.edit_message_text(text="Unknown option selected.")
        return MENU

    # Update user category
    update_user_category(context._chat_id, query.data)

    # Send first quote
    quote = quote_for_specific_user(context._chat_id)
    await context.bot.send_message(chat_id=context._chat_id, text=quote)
    return option


async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "You can use the following commands:\n"
        "/start - Start the bot or select the desired category\n"
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
    for user_data in fetch_scheduled_chats():
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
