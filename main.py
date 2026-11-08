import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from pages.cards_page import CardsPage
from pages.study_pages import StudyPage
from dialogs.settings_dialog import SettingsDialog
from database.db import create_tables
from database.queries import get_all_cards, get_cards_for_repetition


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        create_tables()

        uic.loadUi("ui/main_window_page.ui", self)
        self.cardsPage = CardsPage()
        self.studyPage = StudyPage()

        self.logoIconLabel.setPixmap(QIcon("icons/brain.svg").pixmap(30, 30))
        self.homeIconLabel.setPixmap(QIcon("icons/house.svg").pixmap(30, 30))
        self.cardsIconLabel.setPixmap(QIcon("icons/playing-cards-fan.svg").pixmap(30, 30))
        self.studyIconLabel.setPixmap(QIcon("icons/book-open.svg").pixmap(30, 30))
        self.statsIconLabel.setPixmap(QIcon("icons/trending-up.svg").pixmap(30, 30))
        self.settingsIconLabel.setPixmap(QIcon("icons/settings.svg").pixmap(30, 30))

        self.cardsPage.cards_changed.connect(self.studyPage.refresh_page)
        self.cardsPage.cards_changed.connect(self.fill_information_about_cards)
        self.studyPage.cards_changed.connect(lambda: self.cardsPage.load_cards(get_all_cards()))
        self.studyPage.cards_changed.connect(self.fill_information_about_cards)

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

        self.settingsDialog = SettingsDialog(self)
        self.settingsButton.clicked.connect(self.settingsDialog.exec)

        self.fill_information_about_cards()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(60 * 1000)

    def fill_information_about_cards(self):
        all_cards = get_all_cards()
        cards_for_repetition = get_cards_for_repetition()
        self.quantity_allCardsLabel.setText(f"Всего: {len(all_cards)}")
        self.quantity_repetitionCardsLabel.setText(f"Готовы к повторению: {len(cards_for_repetition)}")

    def update_data(self):
        self.fill_information_about_cards()
        self.studyPage.check_for_new_cards()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(SettingsDialog.load_style("light"))
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())