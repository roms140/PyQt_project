from PyQt6.QtWidgets import QDialog, QApplication
from PyQt6.QtCore import pyqtSignal, QSettings
from PyQt6 import uic
from paths import resource_path


class SettingsDialog(QDialog):
    goal_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(str(resource_path("ui/settings_dialog.ui")), self)

        settings = QSettings("Recall", "Recall")
        goal = settings.value("daily_goal", 20, type=int)

        radio_buttons = {10: self.radioButton10, 20: self.radioButton20,
                         30: self.radioButton30, 40: self.radioButton40}
        radio_buttons[goal].setChecked(True)

        self.radioButton10.toggled.connect(
            lambda checked: self.goal_changed.emit(10) if checked else None
        )
        self.radioButton20.toggled.connect(
            lambda checked: self.goal_changed.emit(20) if checked else None
        )
        self.radioButton30.toggled.connect(
            lambda checked: self.goal_changed.emit(30) if checked else None
        )
        self.radioButton40.toggled.connect(
            lambda checked: self.goal_changed.emit(40) if checked else None
        )

        self.light_themeButton.clicked.connect(self.set_light_theme)
        self.dark_themeButton.clicked.connect(self.set_dark_theme)

    @staticmethod
    def load_style(theme):
        with open(resource_path(f"styles/{theme}_theme.qss"), "r", encoding="utf8") as f:
            return f.read()

    def set_light_theme(self):
        QApplication.instance().setStyleSheet(self.load_style("light"))

        self.light_themeButton.setEnabled(False)
        self.dark_themeButton.setEnabled(True)

    def set_dark_theme(self):
        QApplication.instance().setStyleSheet(self.load_style("dark"))

        self.dark_themeButton.setEnabled(False)
        self.light_themeButton.setEnabled(True)
