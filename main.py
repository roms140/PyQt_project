import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from pages.cards_page import CardsPage
from pages.study_page import StudyPage
from pages.statistics_page import StatisticsPage
from dialogs.settings_dialog import SettingsDialog
from database.db import create_tables
from database.queries import get_cards_count, get_cards_for_repetition, get_all_cards
from collections import Counter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        create_tables()

        uic.loadUi("ui/main_window_page.ui", self)
        self.cardsPage = CardsPage()
        self.studyPage = StudyPage()
        self.statisticsPage = StatisticsPage()

        self.logoIconLabel.setPixmap(QIcon("icons/brain.svg").pixmap(30, 30))
        self.homeIconLabel.setPixmap(QIcon("icons/house.svg").pixmap(30, 30))
        self.cardsIconLabel.setPixmap(
            QIcon("icons/playing-cards-fan.svg").pixmap(30, 30))
        self.studyIconLabel.setPixmap(
            QIcon("icons/book-open.svg").pixmap(30, 30))
        self.statsIconLabel.setPixmap(
            QIcon("icons/trending-up.svg").pixmap(30, 30))
        self.settingsIconLabel.setPixmap(
            QIcon("icons/settings.svg").pixmap(30, 30))

        self.cardsPage.cards_changed.connect(self.studyPage.refresh_page)
        self.cardsPage.cards_changed.connect(self.fill_information_about_cards)
        self.cardsPage.cards_changed.connect(self.statisticsPage.update_data)
        self.cardsPage.cards_changed.connect(
            self.fill_information_about_nearest_repetitions)
        self.studyPage.cards_changed.connect(
            lambda: self.cardsPage.load_cards(get_all_cards()))
        self.studyPage.cards_changed.connect(self.fill_information_about_cards)
        self.studyPage.cards_changed.connect(self.statisticsPage.update_data)
        self.studyPage.cards_changed.connect(
            self.fill_information_about_nearest_repetitions)

        self.stackedWidget.addWidget(self.cardsPage)
        self.stackedWidget.addWidget(self.studyPage)
        self.stackedWidget.addWidget(self.statisticsPage)

        self.homeButton.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(0)
        )

        self.cardsButton.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(1)
        )

        self.studyButton.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(2)
        )

        self.statsButton.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(3))

        self.startStudyButton.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(2))

        self.settingsDialog = SettingsDialog(self)
        self.settingsButton.clicked.connect(self.settingsDialog.exec)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(60 * 1000)
        self.fill_information_about_cards()
        self.fill_information_about_nearest_repetitions()

    def fill_information_about_cards(self):
        count_all_cards = get_cards_count()
        cards_for_repetition = get_cards_for_repetition()
        self.quantity_allCardsLabel.setText(f"Всего: {count_all_cards}")
        self.quantity_repetitionCardsLabel.setText(
            f"Готовы к повторению: {len(cards_for_repetition)}")

    def update_data(self):
        self.fill_information_about_cards()
        self.studyPage.check_for_new_cards()

    def fill_information_about_nearest_repetitions(self):
        self.firtstCardCategoryLabel.show()
        self.secondCardCategoryLabel.show()
        self.thirdCardCategoryLabel.show()
        self.noRepetitionsLabel.hide()
        self.firtstCardCategoryLabel.clear()
        self.secondCardCategoryLabel.clear()
        self.thirdCardCategoryLabel.clear()

        cards = get_cards_for_repetition()
        category_counts = Counter(card[3].lower()
                                  for card in cards).most_common()

        if not category_counts:
            self.firtstCardCategoryLabel.hide()
            self.secondCardCategoryLabel.hide()
            self.thirdCardCategoryLabel.hide()
            self.noRepetitionsLabel.show()
            self.noRepetitionsLabel.setText("Пока нет карточек для повторения")
            return

        for i, category_count in enumerate(category_counts[:3], start=1):
            category = category_count[0].capitalize()
            value = category_count[1]
            if i == 1:
                self.firtstCardCategoryLabel.setText(f"{category}: {value}")
            elif i == 2:
                self.secondCardCategoryLabel.setText(f"{category}: {value}")
            elif i == 3:
                self.thirdCardCategoryLabel.setText(f"{category}: {value}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(SettingsDialog.load_style("light"))
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
