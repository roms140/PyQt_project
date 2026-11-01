import io
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QHeaderView, QStackedWidget
import sqlite3
from pages.cards_page import CardsPage
from pages.study_pages import StudyPage
from database.db import create_tables


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        create_tables()

        uic.loadUi("ui/main_window_page.ui", self)
        self.cardsPage = CardsPage()
        self.studyPage = StudyPage()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
