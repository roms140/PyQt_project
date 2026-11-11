from PyQt6.QtWidgets import QMainWindow, QHeaderView, QTableWidgetItem, QAbstractItemView, QMessageBox, QFileDialog
from PyQt6 import uic
from database.queries import (add_card as db_add_card, get_all_cards, delete_card as db_delete_card,
                              edit_card as db_edit_card, get_all_categories, get_cards_for_export)
from datetime import datetime
from dialogs.card_dialog import CardDialog
from PyQt6.QtCore import Qt, pyqtSignal
import csv


class CardsPage(QMainWindow):
    cards_changed = pyqtSignal()

    def __init__(self):
        super().__init__()

        uic.loadUi("ui/cards_page.ui", self)

        # Настройка таблицы
        self.cardsTableWidget.setHorizontalHeaderLabels(
            ["Вопрос", "Категория", "Следующее повторение"])
        header = self.cardsTableWidget.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.cardsTableWidget.setColumnWidth(0, 400)

        self.cardsTableWidget.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.cardsTableWidget.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.cardsTableWidget.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.addButton.clicked.connect(self.add_card)
        self.editButton.clicked.connect(self.edit_card)
        self.deleteButton.clicked.connect(self.delete_card)
        self.searchLineEdit.textChanged.connect(self.search_cards)
        self.categoryComboBox.currentTextChanged.connect(self.search_cards)
        self.exportCardsButton.clicked.connect(self.export_cards)
        self.importCardsButton.clicked.connect(self.import_cards)

        self.load_cards(get_all_cards())
        self.load_categories()

    def load_categories(self):
        categories = get_all_categories()

        self.categoryComboBox.clear()
        self.categoryComboBox.addItem("Все категории")

        unique_categories = {}
        for c in categories:
            unique_categories[c[0].lower()] = c[0].capitalize()

        for category in sorted(unique_categories.values()):
            self.categoryComboBox.addItem(category)

    def load_cards(self, cards):
        self.cardsTableWidget.setRowCount(len(cards))
        for i, card in enumerate(cards):
            for j, value in enumerate(card[1:]):
                if j == 0:
                    item = QTableWidgetItem(str(value))
                    item.setData(Qt.ItemDataRole.UserRole, card[0])
                elif j == 2:
                    date = datetime.fromisoformat(value)
                    value = f"{date.day} {date.strftime("%B %Y в %H:%M")}"
                    item = QTableWidgetItem(value)
                else:
                    item = QTableWidgetItem(str(value))
                self.cardsTableWidget.setItem(i, j, item)

    def search_cards(self):
        text = self.searchLineEdit.text().lower()
        selected_category = self.categoryComboBox.currentText()
        cards = get_all_cards()
        filtered_cards = [card for card in cards if text.lower() in card[1].lower() and (
            selected_category == "Все категории" or selected_category.lower() == card[2].lower())]
        self.load_cards(filtered_cards)

    def add_card(self):
        dialog = CardDialog(self)
        if dialog.exec():
            question, answer, category, image_data = dialog.card_data

            db_add_card(question, answer, category, image_data)
            self.load_cards(get_all_cards())
            self.load_categories()
            self.cards_changed.emit()

    def edit_card(self):
        row = self.cardsTableWidget.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Ошибка", "Ничего не выделено!")
            return
        card_id = self.cardsTableWidget.item(
            row, 0).data(Qt.ItemDataRole.UserRole)
        dialog = CardDialog(self, card_id)
        if dialog.exec():
            question, answer, category, image_data = dialog.card_data
            db_edit_card(card_id, question, answer, category, image_data)
            self.load_cards(get_all_cards())
            self.load_categories()
            self.cards_changed.emit()

    def delete_card(self):
        row = self.cardsTableWidget.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Ошибка", "Ничего не выделено!")
            return
        valid = QMessageBox.question(
            self,
            'Удаление карточки',
            "Удалить выделенную карточку?",
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if valid == QMessageBox.StandardButton.Yes:
            card_id = self.cardsTableWidget.item(row, 0).data(
                Qt.ItemDataRole.UserRole)
            db_delete_card(card_id)
            self.load_cards(get_all_cards())
            self.load_categories()
            self.cards_changed.emit()

    def export_cards(self):
        cards = get_cards_for_export()

        if not cards:
            QMessageBox.information(
                self, "Экспорт карточек", "Нет карточек для экспорта.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить карточки в CSV", "cards.csv", "CSV files (*.csv)")

        if not file_path:
            return

        if not file_path.lower().endswith(".csv"):
            file_path += ".csv"

        fieldnames = ["question", "answer", "category"]
        try:
            with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for card in cards:
                    writer.writerow(
                        {"question": card[0], "answer": card[1], "category": card[2]})

            QMessageBox.information(
                self,
                "Экспорт карточек",
                f"Успешно экспортировано карточек: {len(cards)}"
            )
        except OSError as e:
            QMessageBox.critical(self, "Ошибка экспорта",
                                 f"Не удалось сохранить файл:\n{e}")

    def import_cards(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите CSV-файл", "", "CSV files (*.csv)")

        if not file_path:
            return

        try:
            with open(file_path, "r", newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)

                expected_headers = ["question", "answer", "category"]
                if reader.fieldnames != expected_headers:
                    QMessageBox.warning(
                        self, "Ошибка импорта", "Неверный формат CSV-файла.")
                    return

                rows = list(reader)

                if not rows:
                    QMessageBox.warning(
                        self, "Ошибка импорта", "В файле отсутствуют карточки")
                    return

                for row_number, row in enumerate(rows, start=2):
                    for key in expected_headers:
                        if not (row[key] or "").strip():
                            QMessageBox.warning(
                                self, "Ошибка импорта", f"В строке {row_number} есть пустые поля.")
                            return

                for row in rows:
                    db_add_card(row["question"].strip(),
                                row["answer"].strip(),
                                row["category"].strip(),
                                None)
                self.load_cards(get_all_cards())
                self.load_categories()
                self.cards_changed.emit()

                QMessageBox.information(
                    self,
                    "Импорт карточек",
                    f"Успешно импортировано карточек: {len(rows)}"
                )

        except (OSError, UnicodeDecodeError, csv.Error) as e:
            QMessageBox.critical(self, "Ошибка импорта",
                                 f"Не удалось прочитать CSV файл:\n{e}")
