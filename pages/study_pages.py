from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from database.queries import get_all_cards, get_cards_for_repetition, add_review_history, update_card_review


class StudyPage(QMainWindow):
    cards_changed = pyqtSignal()

    def __init__(self):
        super().__init__()

        uic.loadUi("ui/study_page.ui", self)

        self.refresh_page()
        self.showAnswerButton.clicked.connect(self.show_answer)
        self.againButton.clicked.connect(lambda : self.next_card("again"))
        self.hardButton.clicked.connect(lambda : self.next_card("hard"))
        self.goodButton.clicked.connect(lambda : self.next_card("good"))
        self.easyButton.clicked.connect(lambda : self.next_card("easy"))

    def refresh_page(self):
        """Обновляет страницу обучения в зависимости от доступных карточек."""
        self.cards = get_all_cards()

        if not self.cards:
            self.statusLabel.setText(
                "У тебя пока нет карточек. Создай их в разделе «Мои карточки».")
            self.show_empty_state()
            return

        self.cards_for_repetition = get_cards_for_repetition()

        if not self.cards_for_repetition:
            self.statusLabel.setText(
                "Пока нет карточек для повторения. Возвращайся позже!")
            self.show_empty_state()
            return

        self.questionFrame.show()
        self.showAnswerButton.show()
        self.ratingFrame.show()
        self.statusLabel.hide()

        self.current_card_index = 0
        self.show_card()

    def show_empty_state(self):
        self.questionFrame.hide()
        self.showAnswerButton.hide()
        self.ratingFrame.hide()
        self.statusLabel.show()

    def show_card(self):
        """Отображает текущую карточку для повторения."""
        if self.current_card_index >= len(self.cards_for_repetition):
            self.refresh_page()
            return
        self.showAnswerButton.setEnabled(True)
        self.current_card = self.cards_for_repetition[self.current_card_index]

        self.questionLabel.setText(self.current_card[1])
        self.answerLabel.setText(self.current_card[2])

        # Скрываем ответ и оценки перед отображением следующей карточки
        self.answerLabel.hide()
        self.ratingFrame.hide()

    def show_answer(self):
        self.answerLabel.show()
        self.ratingFrame.show()
        self.showAnswerButton.setEnabled(False)

    def next_card(self, rating):
        """Добаление истории повторения в БД"""
        if rating == "again":
            interval_minutes = 10
        elif rating == "hard":
            interval_minutes = 24 * 60
        elif rating == "good":
            interval_minutes = 3 * 24 * 60
        elif rating == "easy":
            interval_minutes =  7 * 24 * 60
        card_id = self.current_card[0]
        update_card_review(card_id, interval_minutes)
        add_review_history(card_id, rating, interval_minutes)

        self.cards_changed.emit()

        self.current_card_index += 1
        self.show_card()