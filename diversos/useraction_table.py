import sqlite3

conn = sqlite3.connect("db/dbcad.db", check_same_thread=False)


def create_table():
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NO EXISTS users(id INTEGER PRIMARY KEU AUTOINCREMENT,
        name TEXT,
        contact TEXT,
        age INTEGER,
        gender TEXT,
        email TEXT,
        address TEXT
        """
    )

    conn.commit()
