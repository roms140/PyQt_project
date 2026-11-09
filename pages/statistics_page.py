from PyQt6.QtWidgets import QWidget, QCalendarWidget
from PyQt6 import uic
from database.queries import get_reviews_count, get_cards_count, get_today_reviews_count, get_active_days
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QTextCharFormat, QColor


class StatisticsPage(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("ui/statistics_page.ui", self)
        self.calendarWidget.setVerticalHeaderFormat(
            QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader
        )
        self.calendarWidget.setSelectionMode(
            QCalendarWidget.SelectionMode.NoSelection)

        self.marked_dates = []

        self.update_data()

    def update_data(self):
        self.update_counters()
        self.update_daily_goal()
        self.update_calendar()

    def update_counters(self):
        count_cards = get_cards_count()
        count_reviews = get_reviews_count()
        self.totalCardsValueLabel.setText(str(count_cards))
        self.totalReviewValueLabel.setText(str(count_reviews))

    def update_daily_goal(self):
        goal = 20
        today_reviews = get_today_reviews_count()

        self.progressBar.setRange(0, goal)
        self.progressBar.setValue(min(today_reviews, goal))
        self.goalLabel.setText(f"{today_reviews}/{goal}")

    def update_calendar(self):
        for date in self.marked_dates:
            self.calendarWidget.setDateTextFormat(date, QTextCharFormat())
        self.marked_dates.clear()

        days = get_active_days()

        date_format = QTextCharFormat()
        date_format.setBackground(QColor("#7558D9"))
        date_format.setForeground(QColor("white"))

        for day in days:
            date = QDate.fromString(day[0], "yyyy-MM-dd")
            if date.isValid():
                self.calendarWidget.setDateTextFormat(date, date_format)
                self.marked_dates.append(date)
