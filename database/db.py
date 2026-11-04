import sqlite3


def get_connection():
    con = sqlite3.connect("database/recall.db")
    con.execute("PRAGMA foreign_keys = ON")
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

    cur.execute("""CREATE TABLE IF NOT EXISTS review_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    card_id INTEGER NOT NULL, 
    reviewed_at TEXT NOT NULL, 
    rating TEXT NOT NULL, 
    interval_minutes INTEGER NOT NULL, 
    FOREIGN KEY (card_id) REFERENCES cards(id))""")

    con.commit()
    con.close()
