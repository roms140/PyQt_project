from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic


class CardsPage(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("ui/cards_page.ui", self)

        self.addButton.clicked.connect(self.add_card)

    def add_card(self):
        print("Добавляем карточку")