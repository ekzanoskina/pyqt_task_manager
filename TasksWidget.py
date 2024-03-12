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
        # Load the task item UI and apply task-specific styles
        self.ui = uic.loadUi("Task.ui", self)

        # Initialize the task checkbox with provided text and completion state
        self._task = task
        self.task_checkbox = self.ui.checkBox_3

        self.task_checkbox.setText(task.summary)
        self.task_checkbox.setChecked(self._task.done)
        if self._task.done:
            self.task_checkbox.setStyleSheet(self.checked_style)

        # Connect the checkbox state change to the style update method

        self.task_checkbox.stateChanged.connect(self.update_style)
        self.task_checkbox.stateChanged.connect(self.emitDoneSignal)

        # Initialize and configure the close button
        self.close_btn = self.ui.delete_btn
        self.close_btn.clicked.connect(self.emitCloseSignal)

        # Initialize and configure the close button
        self.edit_btn = self.ui.edit_btn
        self.edit_btn.clicked.connect(self.emitEditSignal)

        # Initialize and configure the close button
        self.view_btn = self.ui.view_btn
        self.view_btn.clicked.connect(self.emitViewSignal)

    # Update the task's visual style based on its completion state

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.task_checkbox = self.task_checkbox.setChecked(not self.task_checkbox.isChecked())
    def update_style(self):
        if self.task_checkbox.isChecked():
            self.task_checkbox.setStyleSheet(self.checked_style)
        else:
            self.task_checkbox.setStyleSheet(self.unchecked_style)

    # Retrieve the current state and text of the task
    def get_checkbox_state(self):
        return self.task_checkbox.isChecked()

    def get_checkbox_text(self):
        return self.task_checkbox.text()

    # Emit a signal indicating the task should be closed, passing its position
    def emitCloseSignal(self):
        self.closeClicked.emit(self._task)

    def emitEditSignal(self):
        self.editClicked.emit(self._task)

    def emitViewSignal(self):
        self.viewClicked.emit(self._task)

    def emitDoneSignal(self):
        self.doneClicked.emit(self._task, self.task_checkbox.isChecked())

class TasksWidget(QWidget):
    def __init__(self, day=None, parent=None, db=None):
        super().__init__(parent)

        self.db = db
        self.parent = parent
        self.ui = uic.loadUi("TasksWidget.ui", self)
        self.selected_date = day

        self.ui.all_btn.clicked.connect(self.show_all_tasks)
        self.ui.active_btn.clicked.connect(self.show_active_tasks)
        self.ui.done_btn.clicked.connect(self.show_done_tasks)
        self.ui.all_btn.setChecked(True)

        self.list_model = QStandardItemModel()  # Model for the task list
        if isinstance(self.selected_date, list):
            self.init_ui(self.ui.tree_view)  # Initialize UI components
        elif isinstance(self.selected_date, date):
            self.init_ui(self.ui.list_view)  # Initialize UI components
        # self.task_list = self.db.get_one_day_tasks(date.today(), None)  # Load tasks from storage
        self.show_tasks()  # Display tasks in the UI

    # Initialize UI components and connect signals
    def init_ui(self, view_option):
        view_option.setModel(self.list_model)
        # view_option.setSpacing(5)
        view_option.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.ui.add_btn.clicked.connect(self.openCreateDialog)

    # Remove a task item from the list
    def remove_item(self, task):
        self.db.delete_task(task)
        self.show_tasks()

    def mark_done(self, task, done_state):
        task.done = done_state
        self.db.save_task(task)
        self.show_tasks()

    def show_all_tasks(self):
        self.show_tasks()

    def show_active_tasks(self):
        self.show_tasks(state_filter=False)

    def show_done_tasks(self):
        self.show_tasks(state_filter=True)

    def show_tasks(self, state_filter=None):
        self.list_model.clear()
        if isinstance(self.selected_date, date):
            self.task_list = self.db.get_one_day_tasks(self.selected_date, state_filter)
            self.ui.tree_view.hide()
        elif isinstance(self.selected_date, list):
            # self.list_model.HorizontalHeaderItem().hide()
            self.ui.list_view.hide()
            self.ui.tree_view.header().hide()
            self.task_list = self.db.get_several_days_tasks(self.selected_date, state_filter)
            tasks_dct ={}
            for task in self.task_list:
                tasks_dct[str(task.scheduled_date)] = tasks_dct.get(str(task.scheduled_date), []) + [task]

            print(tasks_dct)

            for key, value in tasks_dct.items():
                rootNode = self.list_model.invisibleRootItem()
                parent = QStandardItem(key)
                parent.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                for j in range(len(value)):
                    item = QStandardItem()

                    parent.appendRow(item)
                    widget = TaskItem(value[j], db=self.db)
                    widget.closeClicked.connect(self.remove_item)
                    widget.editClicked.connect(self.openEditDialog)
                    widget.viewClicked.connect(self.openViewDialog)
                    widget.doneClicked.connect(self.mark_done)
                    self.ui.tree_view.setIndexWidget(self.list_model.indexFromItem(item), widget)

                rootNode.appendRow(parent)


                # self.tree_view.setIndexWidget(self.list_model.indexFromItem(parent1), widget)
                # index = self.list_model.indexFromItem(parent1)
            # self.ui.tree_view.setRowHidden(0, QModelIndex(), True)
            self.ui.tree_view.expandAll()

                # span container columns
                # self.ui.tree_view.setFirstColumnSpanned(key, self.ui.tree_view.rootIndex(), True)

        for i, task in enumerate(self.task_list):
            item = QStandardItem()
            self.list_model.appendRow(item)
            widget = TaskItem(task, db=self.db)
            widget.closeClicked.connect(self.remove_item)
            widget.editClicked.connect(self.openEditDialog)
            widget.viewClicked.connect(self.openViewDialog)
            widget.doneClicked.connect(self.mark_done)
            item.setSizeHint(widget.sizeHint())

            self.ui.list_view.setIndexWidget(self.list_model.indexFromItem(item), widget)



    def openCreateDialog(self):
        dialog = TaskCreationWidget(self, db=self.db)
        dialog.saveClicked.connect(self.show_tasks)
        dialog.show()

    def openEditDialog(self, task):
        task_edition = TaskEditionWidget(self, db=self.db)
        task_edition.set_task(task)
        task_edition.saveClicked.connect(self.show_tasks)
        task_edition.show()
    def openViewDialog(self, task):
        task_viewing = TaskViewingWidget(self, db=self.db)
        task_viewing.set_task(task)
        task_viewing.editClicked.connect(self.openEditDialog)
        task_viewing.editClicked.connect(lambda: task_viewing.hide())
        task_viewing.show()


    def _redraw_tasks(self):
        """Redraws task widgets."""
        # Clearing all widgets
        for i in range(self._tasks_layout.count()):
            self._tasks_layout.itemAt(i).widget().close()

        for t in sorted(
                self._db.get_tasks(self._current_date),
                key=lambda task: task.scheduled_date
        ):
            self._tasks_layout.addWidget(self._factory.create(t))
    # Save the current tasks to a JSON file when the application is closed.

    def set_selected_date(self, selected_date_datetime):
        self.selected_date = selected_date_datetime
        self.ui.all_btn.setChecked(True)
        self.show_tasks()