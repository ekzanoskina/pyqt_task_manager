from datetime import date
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget

from CustomCalendarWidget import CustomCalendar
from TasksWidget import TasksWidget


class HomePage(QWidget):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)

        self.db = db
        # initialize the view
        self.ui = uic.loadUi("HomePage.ui", self)

        self.ui.selected_date.setText(f'{date.today().strftime("%A")}, {date.today().strftime("%d.%m.%Y")}')
        self.tasks = TasksWidget(parent=self, day=date.today(), db=self.db)
        self.calendar = CustomCalendar(parent=self, db=self.db)

        # adds widgets to the main page layout
        self.ui.tasks_and_calendar_layout.addWidget(self.tasks)
        self.ui.tasks_and_calendar_layout.addWidget(self.calendar)

        # slots and signals connection
        self.calendar.DateChanged.connect(self.set_date_text)
        self.calendar.DateChanged.connect(self.tasks.set_selected_date)

    def set_date_text(self, selected_date_datetime):
        selected_date_str = selected_date_datetime.strftime("%d.%m.%Y")
        selected_date_weekday = selected_date_datetime.strftime("%A")
        self.ui.selected_date.setText(f'{selected_date_weekday}, {selected_date_str}')

    def update(self):
        self.tasks.show_tasks()

