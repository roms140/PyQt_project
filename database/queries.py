from database.db import get_connection


def add_card():
    con = get_connection()
    cur = con.cursor()
    ...


def get_cards_to_review():
    pass


def get_all_cards():
    con = get_connection()
    cur = con.cursor()

    cards = cur.execute(
        "SELECT question, category, next_review_at FROM cards").fetchall()

    con.close()
    return cards


def delete_card():
    pass


def update_card():
    pass


def update_review_date():
    pass
