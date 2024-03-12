from datetime import date, datetime, timedelta
from PyQt6.QtCore import pyqtSignal
from TasksFormTemplate import TaskFormTemplate, DateChoiceDialog


class TaskEditionWidget(TaskFormTemplate):
    """Widget for editing tasks."""
    saveClicked = pyqtSignal()

    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self._db = db
        self.confirm_button.setText('Save')
        self.confirm_button.clicked.connect(self._on_edit)

        self._task = None

        self.summary_line_edit.textChanged.connect(self._enforce_task_change)
        self.description_text_edit.textChanged.connect(self._enforce_task_change)
        self.with_notification.clicked.connect(self._enforce_task_change)
        self.notification_time.timeChanged.connect(self._enforce_task_change)
        self.date_choice.currentTextChanged.connect(self._enforce_task_change)

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


    def _enforce_task_change(self):
        if self._task is None:
            return
        summary = self.summary_line_edit.text()
        descr = self.description_text_edit.toPlainText()
        if self.date_choice.currentIndex() == 0:
            scheduled_date = datetime.now().date()
        elif self.date_choice.currentIndex() == 1:
            scheduled_date = (datetime.now() + timedelta(days=1)).date()
        else:
            scheduled_date = self.picked_date

        if self.with_notification.isChecked():
            notification_time = self.notification_time.time().toPyTime()
        else:
            notification_time = None
        if (summary, descr, scheduled_date, notification_time) == (
                self._task.summary, self._task.description, self._task.scheduled_date, self._task.notification_time
        ):
            self.confirm_button.setEnabled(False)
        else:
            self._enforce_summary_not_empty()

    def _on_edit(self):
        if self._task is None:
            return
        summary = self.summary_line_edit.text()
        descr = self.description_text_edit.toPlainText()
        if self.with_notification.isChecked():
            notification_time = self.notification_time.time().toPyTime()
        else:
            notification_time = None
        self._task.summary = summary
        self._task.description = descr
        self._task.scheduled_date = self.picked_date
        self._task.notification_time = notification_time
        self._db.save_task(self._task)
        self.saveClicked.emit()
        self.close()
