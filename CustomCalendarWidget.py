from PyQt6.QtCore import QPoint, pyqtSignal, Qt
from PyQt6.QtGui import QTextCharFormat, QBrush, QColor
from PyQt6.QtWidgets import QCalendarWidget
from DB import DB
from datetime import date
from PyQt6 import uic


class CustomCalendar(QCalendarWidget):
    DateChanged = pyqtSignal(date)


    def __init__(self, db:DB, parent=None):
        super().__init__(parent)

        self.db = db
        self.parent = parent
        self.selectionChanged.connect(self.calendarDateChanged)

        # Скрыть номер недели слева
        self.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)


        # Изменить цвета субботы и воскресенья
        fmtBlue = QTextCharFormat()
        fmtBlue.setForeground(QBrush(QColor(0, 97, 177)))
        self.setWeekdayTextFormat(Qt.DayOfWeek.Sunday, fmtBlue)
        self.setWeekdayTextFormat(Qt.DayOfWeek.Saturday, fmtBlue)

    def calendarDateChanged(self):
        dateSelected = self.selectedDate().toPyDate()
        self.DateChanged.emit(dateSelected)

    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)
        if date in self.db.get_all_dates():
            painter.setBrush(QColor(0, 0, 85))
            painter.drawEllipse(rect.topRight() + QPoint(-7, 10), 3, 3)