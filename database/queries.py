from database.db import get_connection
from datetime import datetime


def add_card(question, answer, category):
    con = get_connection()
    cur = con.cursor()
    now = datetime.now()
    created_at = now.isoformat(timespec="seconds")
    request = """INSERT INTO cards (question, answer, category, 
    created_at, next_review_at, interval_minutes)
    VALUES (?, ?, ?, ?, ?, ?)"""
    cur.execute(request, (question, answer, category, created_at, created_at, 0))
    con.commit()
    con.close()


def get_data_card(card_id):
    con = get_connection()
    cur = con.cursor()

    card = cur.execute(
        "SELECT question, answer, category FROM cards WHERE id = ?", (card_id,)).fetchone()

    con.close()
    return card


def get_cards_for_repetition():
    con = get_connection()
    cur = con.cursor()

    now = datetime.now()
    current_date = now.isoformat(timespec="seconds")

    request = """SELECT id, question, answer, category, next_review_at 
    FROM cards 
    WHERE next_review_at <= ?
    ORDER BY next_review_at ASC"""
    cards = cur.execute(request, (current_date,)).fetchall()

    con.close()
    return cards


def get_all_cards():
    con = get_connection()
    cur = con.cursor()

    cards = cur.execute(
        "SELECT id, question, category, next_review_at FROM cards").fetchall()

    con.close()
    return cards


def get_all_categories():
    con = get_connection()
    cur = con.cursor()

    categories = cur.execute("SELECT DISTINCT category FROM cards").fetchall()

    con.close()
    return categories


def delete_card(card_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM cards WHERE id = ?", (card_id,))
    con.commit()
    con.close()


def edit_card(card_id, question, answer, category):
    con = get_connection()
    cur = con.cursor()
    request = """UPDATE cards SET question = ?, answer = ?, category = ? WHERE id = ?"""
    cur.execute(request, (question, answer, category, card_id))
    con.commit()
    con.close()


def update_review_date():
    pass
