from telegram import Update
from telegram.ext import (
    CallbackContext,
    ContextTypes,
)

from src.commands import start_command
from src.constants import MENU, BOT_USERNAME, dict_categories
from src.db_tools import (
    fetch_user_category,
    fetch_scheduled_chats,
    fetch_all_data,
    update_user_category,
)
from src.logic import quote_for_specific_user


def handle_response(text: str, chat_id: int) -> None:
    """Handle user response"""

    formatted_text = text.lower()
    if "quote" in formatted_text:
        return quote_for_specific_user(chat_id)
    elif "debug" in formatted_text:  # TODO remove this line
        fetch_all_data()
        rows = fetch_scheduled_chats()
        print(rows)
    else:
        return "I don't understand what you want to say, please try again."


async def handle_fallback(update: Update, context: CallbackContext) -> int:
    """Handle fallback messages"""

    category = fetch_user_category(update.message.chat.id)
    if category:
        update_user_category(update.message.chat.id, category)
        return dict_categories[category] if category in dict_categories else MENU
    else:
        # If no state, initialize conversation
        await start_command(update, context)
        return MENU


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle messages from users"""

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
