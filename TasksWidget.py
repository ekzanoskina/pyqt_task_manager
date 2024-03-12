from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QWidget
from datetime import date
from Task import Task
from TasksCreationWidget import TaskCreationWidget
from TasksEditionWidget import TaskEditionWidget
from TasksViewingWidget import TaskViewingWidget


class TaskItem(QWidget):
    # Signal to indicate when the task's close, edit or view buttons are clicked
    closeClicked = pyqtSignal(Task)
    editClicked = pyqtSignal(Task)
    viewClicked = pyqtSignal(Task)
    doneClicked = pyqtSignal(Task, bool)

    # CSS styles for checked and unchecked tasks
    checked_style = "text-decoration: line-through;"
    unchecked_style = "text-decoration: none;"

    def __init__(self, task, db=None):
        super().__init__()
        self.db = db
        # Loads the task item UI and apply task-specific styles
        self.ui = uic.loadUi("Task.ui", self)

        # Initializes the task checkbox with provided text and completion state
        self._task = task
        self.task_checkbox = self.ui.checkBox_3
        self.task_checkbox.setText(task.summary)
        self.task_checkbox.setChecked(self._task.done)
        if self._task.done:
            self.task_checkbox.setStyleSheet(self.checked_style)

        # Connects the checkbox state change to the style update method
        self.task_checkbox.stateChanged.connect(self.update_style)
        self.task_checkbox.stateChanged.connect(self.emitDoneSignal)

        # Initializes and configures the close button
        self.close_btn = self.ui.delete_btn
        self.close_btn.clicked.connect(self.emitCloseSignal)

        # Initializes and configure the close button
        self.edit_btn = self.ui.edit_btn
        self.edit_btn.clicked.connect(self.emitEditSignal)

        # Initializes and configures the close button
        self.view_btn = self.ui.view_btn
        self.view_btn.clicked.connect(self.emitViewSignal)


    def mousePressEvent(self, event):
        """Detects all mouse clicks on a task item"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.task_checkbox = self.task_checkbox.setChecked(not self.task_checkbox.isChecked())
    def update_style(self):
        """Updates the task's visual style based on its completion state"""
        if self.task_checkbox.isChecked():
            self.task_checkbox.setStyleSheet(self.checked_style)
        else:
            self.task_checkbox.setStyleSheet(self.unchecked_style)

    # @staticmethod
    # def truncate(string, width):
    #     if len(string) > width:
    #         string = string[:width - 3] + '...'
    #     return string

    def emitCloseSignal(self):
        """Emits a signal indicating the task should be closed, passing its object"""
        self.closeClicked.emit(self._task)

    def emitEditSignal(self):
        """Emits a signal that the user wants to edit a task and passes its object"""
        self.editClicked.emit(self._task)

    def emitViewSignal(self):
        """Emits a signal that the user wants to view a task and passes its object"""
        self.viewClicked.emit(self._task)

    def emitDoneSignal(self):
        """Emits a signal that the task has been done"""
        self.doneClicked.emit(self._task, self.task_checkbox.isChecked())

class TasksWidget(QWidget):

    # emits signal that one of the task lists has been changed
    task_view_updates = pyqtSignal()

    def __init__(self, day=None, parent=None, db=None):
        super().__init__(parent)

        self.db = db
        self.parent = parent
        self.ui = uic.loadUi("TasksWidget.ui", self)

        # Sets an initial state
        self.selected_date = day
        self.ui.all_btn.setChecked(True)


        self.init_ui()
        self.list_model = QStandardItemModel()
        self.create_model()
        self.show_tasks()  # Display tasks in the UI

    #
    def init_ui(self):
        """Initializes UI components and connect signals"""
        self.ui.add_btn.clicked.connect(self.openCreateDialog)
        self.ui.all_btn.clicked.connect(self.show_all_tasks)
        self.ui.active_btn.clicked.connect(self.show_active_tasks)
        self.ui.done_btn.clicked.connect(self.show_done_tasks)

    def create_model(self):
        """Creates a model for the task list"""
        self.ui.tree_view.setModel(self.list_model)
        self.ui.tree_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)


    def remove_item(self, task):
        """Removes a task item from the list"""
        self.db.delete_task(task)
        self.show_tasks()
        self.other_lists_update()

    def mark_done(self, task, done_state):
        """Marks a task as done"""
        task.done = done_state
        self.db.save_task(task)
        self.show_tasks()
        self.other_lists_update()

    def show_all_tasks(self):
        self.show_tasks()

    def show_active_tasks(self):
        """Shows active tasks"""
        self.show_tasks(state_filter=False)

    def show_done_tasks(self):
        """Shows done tasks"""
        self.show_tasks(state_filter=True)

    def show_tasks(self, state_filter=None):
        self.list_model.clear()
        if isinstance(self.selected_date, date):
            self.task_list = self.db.get_one_day_tasks(self.selected_date, state_filter)
            for i, task in enumerate(self.task_list):
                item = QStandardItem()
                self.list_model.appendRow(item)
                widget = self.task_widget_creation(task)
                item.setSizeHint(widget.sizeHint())
                self.ui.tree_view.setIndexWidget(self.list_model.indexFromItem(item), widget)
        elif isinstance(self.selected_date, list):
            self.task_list = self.db.get_several_days_tasks(self.selected_date, state_filter)
            tasks_dct = {}
            for task in self.task_list:
                tasks_dct[self.format_date(task.scheduled_date)] = tasks_dct.get(self.format_date(task.scheduled_date), []) + [task]

            for key, tasks in tasks_dct.items():
                rootNode = self.list_model.invisibleRootItem()
                parent = QStandardItem(key)
                parent.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                for task in tasks:
                    item = QStandardItem()
                    parent.appendRow(item)
                    widget = self.task_widget_creation(task)
                    item.setSizeHint(widget.sizeHint())
                    self.ui.tree_view.setIndexWidget(self.list_model.indexFromItem(item), widget)
                rootNode.appendRow(parent)
            self.ui.tree_view.expandAll()

    def task_widget_creation(self, task):
        widget = TaskItem(task, db=self.db)
        widget.closeClicked.connect(self.remove_item)
        widget.editClicked.connect(self.openEditDialog)
        widget.viewClicked.connect(self.openViewDialog)
        widget.doneClicked.connect(self.mark_done)
        return widget


    def format_date(self, selected_date_datetime):
        """Changes the date format"""
        selected_date_str = selected_date_datetime.strftime("%d.%m.%Y")
        selected_date_weekday = selected_date_datetime.strftime("%A")
        return f'{selected_date_weekday}, {selected_date_str}'


    def openCreateDialog(self):
        dialog = TaskCreationWidget(self, db=self.db)
        dialog.saveClicked.connect(self.show_tasks)
        dialog.saveClicked.connect(self.other_lists_update)
        dialog.show()

    def openEditDialog(self, task):
        task_edition = TaskEditionWidget(self, db=self.db)
        task_edition.set_task(task)
        task_edition.saveClicked.connect(self.show_tasks)
        task_edition.saveClicked.connect(self.other_lists_update)
        task_edition.show()

    def openViewDialog(self, task):
        task_viewing = TaskViewingWidget(self, db=self.db)
        task_viewing.set_task(task)
        task_viewing.editClicked.connect(self.openEditDialog)
        task_viewing.editClicked.connect(lambda: task_viewing.hide())
        task_viewing.show()

    def set_selected_date(self, selected_date_datetime):
        self.selected_date = selected_date_datetime
        self.ui.all_btn.setChecked(True)
        self.show_tasks()

    def other_lists_update(self):
        self.task_view_updates.emit()