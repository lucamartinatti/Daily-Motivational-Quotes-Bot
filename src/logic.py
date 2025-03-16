import pandas as pd
import random

from src.db_tools import get_user_category, get_scheduled_chat, fetch_all_data


def handle_response(text: str, chat_id: int) -> None:
    formatted_text = text.lower()
    if "quote" in formatted_text:
        return quote_for_specific_user(chat_id)
    elif "debug" in formatted_text:  # TODO remove this line
        fetch_all_data()
        rows = get_scheduled_chat()
        print(rows)
    else:
        return "I don't understand what you want to say, please try again."


def quote_for_specific_user(chat_id: int) -> str:
    category = get_user_category(chat_id)
    quote = get_quote(category)
    return quote


def get_quote(category: str | None = None) -> str:
    df = pd.read_csv("./data/dataset.csv")

    if category:
        df = df[df["category"].str.contains(category, case=False, na=False)]

    if df.empty:
        return "No quotes found, check their presence in the dataset."

    # select a random quote
    random_row = random.choice(df.index)

    quote = df.loc[random_row, "quote"]
    if not quote.endswith("."):
        quote += "."

    author = df.loc[random_row, "author"]

    if author == "Unknown" or pd.isnull(author) or author == "":
        author = "Unknown"

    return f'"{quote}" - {author}'
