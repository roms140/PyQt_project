from PyQt6.QtWidgets import QMainWindow, QHeaderView, QTableWidgetItem, QAbstractItemView, QMessageBox
from PyQt6 import uic
from database.queries import add_card as db_add_card, get_all_cards, delete_card as db_delete_card
from dialogs.card_dialog import CardDialog
from PyQt6.QtCore import Qt


class CardsPage(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("ui/cards_page.ui", self)

        self.cardsTableWidget.setHorizontalHeaderLabels(
            ["Вопрос", "Категория", "Следующее повторение"])
        header = self.cardsTableWidget.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        self.cardsTableWidget.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.cardsTableWidget.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.load_cards()

        self.addButton.clicked.connect(self.add_card)
        self.deleteButton.clicked.connect(self.delete_card)

    def load_cards(self):
        cards = get_all_cards()
        self.cardsTableWidget.setRowCount(len(cards))
        for i, card in enumerate(cards):
            for j, value in enumerate(card[1:]):
                if j == 0:
                    item = QTableWidgetItem(str(value))
                    item.setData(Qt.ItemDataRole.UserRole, card[0])
                else:
                    item = QTableWidgetItem(str(value))
                self.cardsTableWidget.setItem(i, j, item)

    def add_card(self):
        dialog = CardDialog(self)
        if dialog.exec():
            question, answer, category = dialog.card_data

            db_add_card(question, answer, category)
            self.load_cards()

    def delete_card(self):
        row = self.cardsTableWidget.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Ошибка", "Ничего не выделено!")
            return
        valid = QMessageBox.question(
            self,
            'Удаление карточки',
            "Удалить эту карточку?",
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if valid == QMessageBox.StandardButton.Yes:
            card_id = self.cardsTableWidget.item(row, 0).data(
                Qt.ItemDataRole.UserRole)
            db_delete_card(card_id)
            self.load_cards()