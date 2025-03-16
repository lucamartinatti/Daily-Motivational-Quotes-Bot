import os
from typing import Final
from dotenv import load_dotenv

load_dotenv()

TOKEN: Final = os.getenv("TOKEN")
BOT_USERNAME: Final = os.getenv("BOT_USERNAME")

MENU, OPTION1, OPTION2, OPTION3, OPTION4, OPTION5 = range(6)

dict_categories = {
    "motivation": 1,
    "philosophy": 2,
    "stoic": 3,
    "life": 4,
    "love": 5,
}
