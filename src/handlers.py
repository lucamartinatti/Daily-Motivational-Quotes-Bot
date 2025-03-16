from telegram import Update
from telegram.ext import (
    CallbackContext,
    ContextTypes,
)

from src.constants import MENU, BOT_USERNAME
from src.db_tools import get_user_category
from src.logic import handle_response


async def handle_fallback(update: Update, context: CallbackContext) -> int:
    # Check if user exists in the database

    if get_user_category(update.message.chat.id):
        current_state = context.user_data["state"]
        await update.message.reply_text(f"Resuming from state: {current_state}")
        return current_state
    else:
        # If no state, initialize conversation
        await update.message.reply_text("Welcome back! Please choose an option.")
        return MENU


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_type = update.message.chat.type
    text = update.message.text

    print(
        f"User: {update.message.chat.id} - Received message: {text} - Message type: {message_type}"
    )

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, "").strip()
            response = handle_response(new_text, update.message.chat.id)
        else:
            return
    else:
        response = handle_response(text, update.message.chat.id)

    print(f"Bot response: {response}")

    await update.message.reply_text(response)


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"This update: {update} causes the following error: {context.error}")
