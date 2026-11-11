from PyQt6.QtWidgets import QDialog, QMessageBox, QFileDialog
from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
from database.queries import get_data_card as db_get_data_card


class CardDialog(QDialog):
    def __init__(self, parent=None, id_card=None):
        super().__init__(parent)
        uic.loadUi("ui/card_dialog.ui", self)

        self.imageLabel.setPixmap(QIcon("icons/image-plus.svg").pixmap(65, 65))

        self.questionLineEdit.setMaxLength(100)
        self.categoryLineEdit.setMaxLength(40)

        self.saveButton.clicked.connect(self.save_card)
        self.chooseImageButton.clicked.connect(self.choose_image)
        self.deleteImageButton.clicked.connect(self.delete_image)
        self.deleteImageButton.hide()
        self.image_data = None

        self.id_card = id_card
        if id_card is not None:
            self.saveButton.setText("Отредактировать")
            self.setWindowTitle("Редактирование карты")
            self.get_data_card()

    def get_data_card(self):
        question, answer, category, image_data = db_get_data_card(self.id_card)

        self.questionLineEdit.setText(question)
        self.answerPlainTextEdit.setPlainText(answer)
        self.categoryLineEdit.setText(category)
        self.image_data = image_data

        if self.image_data:
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)

            self.imageLabel.setPixmap(pixmap.scaled(
                100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.deleteImageButton.show()

    def save_card(self):
        question = self.questionLineEdit.text().strip()
        answer = self.answerPlainTextEdit.toPlainText().strip()
        category = self.categoryLineEdit.text().strip()

        if not question or not answer or not category:
            QMessageBox.warning(
                self, "Ошибка", "Все поля должны быть заполнены!")
            return

        self.card_data = (question, answer, category, self.image_data)
        self.accept()

    def choose_image(self):
        image_path, _ = QFileDialog.getOpenFileName(
            self, "Выбрать изображение", "", "Images (*.png *.jpg *.jpeg)")
        if image_path:
            with open(image_path, "rb") as f:
                self.image_data = f.read()

            pixmap = QPixmap(image_path)
            pixmap.loadFromData(self.image_data)

            self.imageLabel.setPixmap(pixmap.scaled(
                100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.deleteImageButton.show()

    def delete_image(self):
        if self.image_data is None:
            return

        self.imageLabel.setPixmap(QIcon("icons/image-plus.svg").pixmap(65, 65))
        self.image_data = None
        self.deleteImageButton.hide()

