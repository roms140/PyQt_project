import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QCheckBox, QPlainTextEdit


class MacOrder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 150, 350, 400)
        self.setWindowTitle("Заказ в Макдональдсе")

        self.cheeseburger = QCheckBox("Чизбургер", self)
        self.cheeseburger.move(10, 0)
        self.hamburger = QCheckBox("Гамбургер", self)
        self.hamburger.move(10, 25)
        self.kola = QCheckBox("Кока-кола", self)
        self.kola.move(10, 50)
        self.nuggets = QCheckBox("Наггетсы", self)
        self.nuggets.move(10, 75)

        self.menu_checkboxes = [self.cheeseburger,
                                self.hamburger, self.kola, self.nuggets]

        self.order_btn = QPushButton("Заказать", self)
        self.order_btn.move(10, 125)
        self.order_btn.clicked.connect(self.show_order)

        self.result = QPlainTextEdit(self)
        self.result.move(10, 160)

    def show_order(self):
        self.result.setPlainText("Ваш заказ:\n")
        for checkbox in self.menu_checkboxes:
            if checkbox.isChecked():
                self.result.appendPlainText(checkbox.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MacOrder()
    ex.show()
    sys.exit(app.exec())
