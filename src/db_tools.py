import sqlite3


def create_table():
    with sqlite3.connect("./database/test.db") as connection:
        print("Opened database successfully")
        cursor = connection.cursor()
        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS userdata (
            id INTEGER NOT NULL PRIMARY KEY UNIQUE,
            first_name TEXT,
            last_name TEXT,
            full_name TEXT,
            username TEXT,
            link TEXT,
            category TEXT,
            automatic BOOLEAN
        );"""
        )
        connection.commit()
        print("Table created successfully")


def insert_user_data(chat):
    try:
        with sqlite3.connect("./database/test.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                """INSERT OR REPLACE INTO userdata (id, first_name, last_name, full_name, username, link,category, automatic) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    chat.id,
                    chat.first_name,
                    chat.last_name,
                    chat.full_name,
                    chat.username,
                    chat.link,
                    "all",
                    True,
                ),
            )
            connection.commit()
        print("User saved successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


def update_user_category(chat_id, category):
    try:
        with sqlite3.connect("./database/test.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE userdata SET category = ? WHERE id = ?", (category, chat_id)
            )
            connection.commit()
        print("Category updated successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


def fetch_all_data():
    try:
        with sqlite3.connect("./database/test.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM userdata")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


def fetch_scheduled_chats():
    try:
        with sqlite3.connect("./database/test.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, category FROM userdata WHERE automatic = 1")
            rows = cursor.fetchall()
            return rows
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []


def fetch_user_category(chat_id):
    try:
        with sqlite3.connect("./database/test.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT category FROM userdata WHERE id = ?", (chat_id,))
            row = cursor.fetchone()
            if row:
                return row[0] if row[0].lower() != "none" else None
            else:
                return None

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
