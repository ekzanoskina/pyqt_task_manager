from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic
from TaskListsPage import TaskListsPage
from DB import DB
from NotesWidget import NotesWidget
from HomePage import HomePage

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = DB()
        # Load the main window UI
        self.ui = uic.loadUi("MainWindow1.ui", self)

        # menu initial state
        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn_2.setChecked(True)

        # home page initialization
        self.home_page = HomePage(db=self.db)
        self.ui.home_page_layout.addWidget(self.home_page)

        # task lists page initialization
        self.task_lists_page = TaskListsPage(db=self.db)
        self.ui.task_lists_page_layout.addWidget(self.task_lists_page)

        # notes page initialization
        notes_widget = NotesWidget(self.db)
        self.ui.notes_layout.addWidget(notes_widget)

    # Functions for changing pages
    def on_search_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        search_text = self.ui.search_input.text().strip()
        if search_text:
            self.ui.label_9.setText(search_text)

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
        self.task_lists_page.update()

    def on_tasks_btn_2_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.task_lists_page.update()

    def on_notes_btn_1_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_notes_btn_2_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)


