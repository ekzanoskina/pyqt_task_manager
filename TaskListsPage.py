from datetime import date, timedelta

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from TasksWidget import TasksWidget


class TaskListsPage(QWidget):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)

        self.db = db
        # initialize the view
        self.ui = uic.loadUi("TaskListsPage.ui", self)


        # creates lists for today, tomorrow, next 7 days
        self.today_tasks = TasksWidget(parent=self, day=date.today(),  db=self.db)
        self.tomorrow_tasks = TasksWidget(parent=self, day=date.today() + timedelta(days=1),  db=self.db)
        self.next_seven_days_tasks = TasksWidget(parent=self, day=[date.today(), date.today()+timedelta(days=7)],  db=self.db)

        # adds them to the layout
        self.ui.task_lists.addWidget(self.today_tasks)
        self.ui.task_lists.addWidget(self.tomorrow_tasks)
        self.ui.task_lists.addWidget(self.next_seven_days_tasks)

        self.one_one_list_change()

    def update(self):
        self.today_tasks.show_tasks()
        self.tomorrow_tasks.show_tasks()
        self.next_seven_days_tasks.show_tasks()

    def one_one_list_change(self):
        self.today_tasks.task_view_updates.connect(self.tomorrow_tasks.show_tasks)
        self.today_tasks.task_view_updates.connect(self.next_seven_days_tasks.show_tasks)
        self.next_seven_days_tasks.task_view_updates.connect(self.today_tasks.show_tasks)
        self.next_seven_days_tasks.task_view_updates.connect(self.tomorrow_tasks.show_tasks)
        self.tomorrow_tasks.task_view_updates.connect(self.today_tasks.show_tasks)
        self.tomorrow_tasks.task_view_updates.connect(self.next_seven_days_tasks.show_tasks)