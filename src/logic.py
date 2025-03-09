import pandas as pd
import random

categories = [
    "motivation",
    "philosophy",
    "stoic",
    "life",
    "love",
]

selected_category = "stoic"


def get_quote():
    df = pd.read_csv("./data/dataset.csv")

    # df = df[df["category"].str.contains(selected_category, case=False, na=False)]
    # select a random quote
    random_row = random.choice(df.index)

    quote = df.loc[random_row, "quote"]
    if not quote.endswith("."):
        quote += "."

    author = df.loc[random_row, "author"]

    if author == "Unknown" or pd.isnull(author) or author == "":
        author = "Unknown"

    return f'"{quote}" - {author}'
