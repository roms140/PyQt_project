from PyQt6.QtWidgets import QDialog, QApplication
from PyQt6 import uic
from paths import resource_path


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(str(resource_path("ui/settings_dialog.ui")), self)

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
