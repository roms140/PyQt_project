import sqlite3


def get_connection():
    con = sqlite3.connect("database/recall.db")
    return con


def create_tables():
    con = get_connection()
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    question TEXT NOT NULL, 
    answer TEXT NOT NULL, 
    category TEXT, 
    created_at TEXT, 
    next_review_at TEXT, 
    interval_minutes INTEGER)""")

    con.commit()
    con.close()
