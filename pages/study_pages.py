from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic


class StudyPage(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("ui/study_page.ui", self)