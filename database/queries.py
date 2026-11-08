from database.db import get_connection
from datetime import datetime, timedelta


def add_card(question, answer, category, image_data):
    con = get_connection()
    cur = con.cursor()
    now = datetime.now()
    created_at = now.isoformat(timespec="seconds")
    request = """INSERT INTO cards (question, answer, category, 
    created_at, next_review_at, interval_minutes, image)
    VALUES (?, ?, ?, ?, ?, ?, ?)"""
    cur.execute(request, (question, answer, category, created_at, created_at, 0, image_data))
    con.commit()
    con.close()


def add_review_history(card_id, rating, interval_minutes):
    con = get_connection()
    cur = con.cursor()
    now = datetime.now()
    reviewed_at = now.isoformat(timespec="seconds")
    request = """INSERT INTO review_history (card_id, reviewed_at, rating, 
    interval_minutes)
    VALUES (?, ?, ?, ?)"""
    cur.execute(request, (card_id, reviewed_at, rating, interval_minutes))
    con.commit()
    con.close()


def get_data_card(card_id):
    con = get_connection()
    cur = con.cursor()

    card = cur.execute(
        "SELECT question, answer, category, image FROM cards WHERE id = ?", (card_id,)).fetchone()

    con.close()
    return card


def get_cards_for_repetition():
    con = get_connection()
    cur = con.cursor()

    now = datetime.now()
    current_date = now.isoformat(timespec="seconds")

    request = """SELECT id, question, answer, category, image 
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
        "SELECT id, question, category, next_review_at FROM cards ORDER BY next_review_at").fetchall()

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


def edit_card(card_id, question, answer, category, image_data):
    con = get_connection()
    cur = con.cursor()
    request = """UPDATE cards SET question = ?, answer = ?, category = ?, image = ? WHERE id = ?"""
    cur.execute(request, (question, answer, category, image_data, card_id))
    con.commit()
    con.close()


def update_card_review(card_id, interval_minutes):
    con = get_connection()
    cur = con.cursor()
    next_review_at = datetime.now() + timedelta(minutes=interval_minutes)
    next_review_at_iso = next_review_at.isoformat(timespec="seconds")
    request = """UPDATE cards SET next_review_at = ?, interval_minutes = ? WHERE id = ?"""
    cur.execute(request, (next_review_at_iso, interval_minutes, card_id))
    con.commit()
    con.close()