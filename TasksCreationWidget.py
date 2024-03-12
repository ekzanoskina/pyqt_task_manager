from PyQt6.QtCore import pyqtSignal

from Task import Task
from TasksFormTemplate import TaskFormTemplate


class TaskCreationWidget(TaskFormTemplate):
    """Widget for creating tasks."""
    saveClicked = pyqtSignal()

    def __init__(self, parent=None, db=None):
        super().__init__(parent)

        self._db = db

        self.setWindowTitle('Task creation')
        self.confirm_button.setText('Save')
        self.confirm_button.clicked.connect(self._on_create)

    def _on_create(self):
        """Creates task."""
        scheduled_date = self.picked_date
        summary = self.summary_line_edit.text()
        descr = self.description_text_edit.toPlainText()
        if self.with_notification.isChecked():
            notification_time = self.notification_time.time().toPyTime()
        else:
            notification_time = None
        task = Task(summary, descr, scheduled_date, notification_time, False)
        self._db.save_task(task)
        self.summary_line_edit.clear()
        self.description_text_edit.clear()
        self.saveClicked.emit()
        self.close()
