from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic
from datetime import date, timedelta
from TasksWidget import TasksWidget
from DB import DB
from NotesWidget import NotesWidget
from CustomCalendarWidget import CustomCalendar
from HomePage import HomePage

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = DB()
        # Load the main window UI
        self.ui = uic.loadUi("MainWindow1.ui", self)
        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn_2.setChecked(True)

        # home page initialization
        self.home_page = HomePage(db=self.db)
        self.ui.home_page_layout.addWidget(self.home_page)

        # lists page initialization

        self.today_tasks = TasksWidget(parent=self, day=date.today(),  db=self.db)
        self.tomorrow_tasks = TasksWidget(parent=self, day=date.today() + timedelta(days=1),  db=self.db)
        self.next_seven_days_tasks = TasksWidget(parent=self, day=[date.today(), date.today()+timedelta(days=7)],  db=self.db)


        self.ui.tasks_lists.addWidget(self.today_tasks)
        self.ui.tasks_lists.addWidget(self.tomorrow_tasks)
        self.ui.tasks_lists.addWidget(self.next_seven_days_tasks)


        notes_widget = NotesWidget(self.db)
        self.ui.notes_layout.addWidget(notes_widget)



    def on_search_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        search_text = self.ui.search_input.text().strip()
        if search_text:
            self.ui.label_9.setText(search_text)


    # Function for changing page to user page
    def on_user_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(6)


    # Functions for changing menu page
    def on_home_btn_1_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.home_page.update()

    def on_home_btn_2_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.home_page.update()

    def on_tasks_btn_1_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.today_tasks.show_tasks()
        self.tomorrow_tasks.show_tasks()
        self.next_seven_days_tasks.show_tasks()


    def on_tasks_btn_2_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.today_tasks.show_tasks()
        self.tomorrow_tasks.show_tasks()
        self.next_seven_days_tasks.show_tasks()

    def on_notes_btn_1_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)


    def on_notes_btn_2_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)


