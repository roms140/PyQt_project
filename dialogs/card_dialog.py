from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from database.queries import get_data_card as db_get_data_card

class CardDialog(QDialog):
    def __init__(self, parent=None, id_card=None):
        super().__init__(parent)
        uic.loadUi("ui/card_dialog.ui", self)
        self.saveButton.clicked.connect(self.save_card)
        self.id_card = id_card
        if id_card is not None:
            self.saveButton.setText("Отредактировать")
            self.setWindowTitle("Редактирование карты")
            self.get_data_card()

    def get_data_card(self):
        question, answer, category = db_get_data_card(self.id_card)
        self.questionLineEdit.setText(question)
        self.answerPlainTextEdit.setPlainText(answer)
        self.categoryLineEdit.setText(category)

    def save_card(self):
        question = self.questionLineEdit.text().strip()
        answer = self.answerPlainTextEdit.toPlainText().strip()
        category = self.categoryLineEdit.text().strip()

        if not question or not answer or not category:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return

        self.card_data = (question, answer, category)
        self.accept()



