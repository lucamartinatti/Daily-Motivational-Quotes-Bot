from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from src.constants import TOKEN, MENU, OPTION1, OPTION2, OPTION3, OPTION4, OPTION5
from src.commands import (
    start_command,
    button,
    help_command,
    quote_command,
    schedule_daily_quote,
)
from src.handlers import handle_fallback, handle_message, handle_error
from src.db_tools import create_table, fetch_all_data


def main():
    print("Start Bot...")

    app = Application.builder().token(TOKEN).build()

    create_table()

    fetch_all_data()

    # Commands
    # app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("quote", quote_command))

    # Message
    # app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error
    app.add_error_handler(handle_error)

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start_command),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
        ],
        states={
            MENU: [
                CallbackQueryHandler(button),
                MessageHandler(filters.TEXT, handle_message),
            ],
            OPTION1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
            OPTION1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
            OPTION2: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
            OPTION3: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
            OPTION4: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
            OPTION5: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
        },
        # fallbacks=[CommandHandler("start", start_command)],
        fallbacks=[MessageHandler(filters.ALL, handle_fallback)],
    )
    app.add_handler(conv_handler)

    # Schedule daily quote
    schedule_daily_quote(app)

    # Run the bot
    print("Polling...")
    app.run_polling(poll_interval=2)


if __name__ == "__main__":
    main()
