from PyQt6.QtWidgets import QMainWindow, QHeaderView
from PyQt6 import uic
from database.queries import add_card as db_add_card


class CardsPage(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("ui/cards_page.ui", self)

        self.cardsTableWidget.setHorizontalHeaderLabels(["Вопрос", "Категория", "Следующее повторение"])
        header = self.cardsTableWidget.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.resizeSection(0, 500)
        header.resizeSection(1, 200)
        header.resizeSection(2, 300)

    def add_card(self):
        pass


