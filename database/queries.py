from database.db import get_connection
from datetime import datetime


def add_card(question, answer, category):
    con = get_connection()
    cur = con.cursor()
    now = datetime.now()
    created_at = now.isoformat(timespec="seconds")
    queue = """INSERT INTO cards (question, answer, category, 
    created_at, next_review_at, interval_minutes)
    VALUES (?, ?, ?, ?, ?, ?)"""
    cur.execute(queue, (question, answer, category, created_at, created_at, 0))
    con.commit()
    con.close()


def get_cards_to_review():
    pass


def get_all_cards():
    con = get_connection()
    cur = con.cursor()

    cards = cur.execute(
        "SELECT id, question, category, next_review_at FROM cards").fetchall()

    con.close()
    return cards


def delete_card(card_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM cards WHERE id = ?", (card_id,))
    con.commit()
    con.close()

def update_card():
    pass


def update_review_date():
    pass
