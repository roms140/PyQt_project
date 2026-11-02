from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic


class CardDialog(QDialog):
    def __init__(self, parent=None, card_data=None):
        super().__init__(parent)
        uic.loadUi("ui/card_dialog.ui", self)
        if card_data is not None:
            self.addButton.clicked.connect(self.edit_card)
            self.addButton.setText("Редактирование карты")
            self.get_data_card()
        else:
            self.addButton.clicked.connect(self.save_card)

    def get_data_card(self):
        pass

    def save_card(self):
        question = self.questionLineEdit.text().strip()
        answer = self.answerPlainTextEdit.toPlainText().strip()
        category = self.categoryLineEdit.text().strip()

        if not question or not answer or not category:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return

        self.card_data = (question, answer, category)
        self.accept()

    def edit_card(self):
        pass



