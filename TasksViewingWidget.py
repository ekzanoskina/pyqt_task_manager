from PyQt6.QtCore import pyqtSignal

from Task import Task
from TasksFormTemplate import TaskFormTemplate
from datetime import datetime, date, timedelta


class TaskViewingWidget(TaskFormTemplate):
    """Widget for editing tasks."""
    editClicked = pyqtSignal(Task)

    def __init__(self, parent=None, db=None):
                 # on_cancel: Callable
        super().__init__(parent)
        self._db = db
        self.confirm_button.setText('Edit')

        self.confirm_button.clicked.connect(self.emitEditSignal)
        self._task = None
        self.summary_line_edit.setReadOnly(True)
        self.description_text_edit.setReadOnly(True)
        self.with_notification.setEnabled(False)
        self.notification_time.setReadOnly(True)
        self.date_choice.setEnabled(False)
        self.confirm_button.setEnabled(True)

    def emitEditSignal(self):
        self.editClicked.emit(self._task)

    def set_task(self, task):
        self._task = task
        self.picked_date = task.scheduled_date
        self.summary_line_edit.setText(task.summary)
        self.description_text_edit.setText(task.description)
        if task.scheduled_date == datetime.now().date():
            self.date_choice.setCurrentIndex(0)
        elif task.scheduled_date == (datetime.now() + timedelta(days=1)).date():
            self.date_choice.setCurrentIndex(1)
        else:
            self.date_choice.setCurrentIndex(2)
            self.date_choice.setItemText(2, str(task.scheduled_date))

        if task.notification_time:
            self.with_notification.setChecked(True)
            self.notification_time.show()
            self.notification_time.setTime(self._task.notification_time)