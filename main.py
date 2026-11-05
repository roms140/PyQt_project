import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer
from pages.cards_page import CardsPage
from pages.study_pages import StudyPage
from database.db import create_tables
from database.queries import get_all_cards, get_cards_for_repetition


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        create_tables()

        uic.loadUi("ui/main_window_page.ui", self)
        self.cardsPage = CardsPage()
        self.studyPage = StudyPage()

        self.cardsPage.cards_changed.connect(self.studyPage.refresh_page)
        self.cardsPage.cards_changed.connect(self.set_quantity_cards_for_repetition)
        self.studyPage.cards_changed.connect(lambda: self.cardsPage.load_cards(get_all_cards()))
        self.studyPage.cards_changed.connect(self.set_quantity_cards_for_repetition)

        self.stackedWidget.addWidget(self.cardsPage)
        self.stackedWidget.addWidget(self.studyPage)
        self.homeButton.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(0)
        )

        self.cardsButton.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(1)
        )

        self.studyButton.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(2)
        )

        self.startStudyButton.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(2))

        self.set_quantity_cards_for_repetition()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(60 * 1000)

    def set_quantity_cards_for_repetition(self):
        cards = get_cards_for_repetition()
        self.quantityCardsLabel.setText(f"Всего карт к повторению: {str(len(cards))}")

    def update_data(self):
        self.set_quantity_cards_for_repetition()
        self.studyPage.check_for_new_cards()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())

