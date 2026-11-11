import sqlite3
import sys
from pathlib import Path


if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "recall.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON")
    return con


def create_tables():
    con = get_connection()
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    question TEXT NOT NULL, 
    answer TEXT NOT NULL, 
    category TEXT NOT NULL, 
    created_at TEXT, 
    next_review_at TEXT, 
    interval_minutes INTEGER, 
    image BLOB)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS review_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    card_id INTEGER NOT NULL, 
    reviewed_at TEXT NOT NULL, 
    rating TEXT NOT NULL, 
    interval_minutes INTEGER NOT NULL, 
    FOREIGN KEY (card_id) REFERENCES cards(id) ON DELETE CASCADE)""")

    con.commit()
    con.close()
