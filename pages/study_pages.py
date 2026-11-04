from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic
from database.queries import get_all_cards, get_cards_for_repetition


class StudyPage(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("ui/study_page.ui", self)

        self.refresh_page()
        self.showAnswerButton.clicked.connect(self.show_answer)
        self.againButton.clicked.connect(self.next_card)
        self.hardButton.clicked.connect(self.next_card)
        self.goodButton.clicked.connect(self.next_card)
        self.easyButton.clicked.connect(self.next_card)

    def refresh_page(self):
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
        if self.current_card_index >= len(self.cards_for_repetition):
            self.refresh_page()
            return
        self.showAnswerButton.setEnabled(True)
        card = self.cards_for_repetition[self.current_card_index]

        self.questionLabel.setText(card[1])
        self.answerLabel.setText(card[2])

        self.answerLabel.hide()
        self.ratingFrame.hide()

    def show_answer(self):
        self.answerLabel.show()
        self.ratingFrame.show()
        self.showAnswerButton.setEnabled(False)

    def next_card(self):
        self.current_card_index += 1
        self.show_card()