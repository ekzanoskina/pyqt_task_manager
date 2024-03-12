from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QCalendarWidget, QVBoxLayout, QDialog, QLineEdit, QTextEdit, \
    QComboBox, QCheckBox, QTimeEdit
from datetime import date, datetime, timedelta


class TaskFormTemplate(QDialog):
    """UI template for creating and editing tasks."""

    def __init__(self, parent=None):
        super(TaskFormTemplate, self).__init__(parent)
        self.setWindowTitle('Task creation')
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.picked_date = datetime.now().date()

        self.summary_line_edit = QLineEdit(placeholderText="Summary",
                                           maxLength=100,
                                           textChanged=self._enforce_summary_not_empty)
        self.description_text_edit = QTextEdit(placeholderText="Description")

        text_layout = QVBoxLayout()
        text_layout.addWidget(self.summary_line_edit)
        text_layout.addWidget(self.description_text_edit)

        self.cancel_button = QPushButton(text="Return")
        self.cancel_button.setAutoDefault(False)
        self.cancel_button.clicked.connect(self.closeDialog)

        self.confirm_button = QPushButton(text='Save', enabled=False)

        self.date_choice = QComboBox()
        self.date_choice.addItems(['today', 'tomorrow', 'choose the date'])
        self.date_choice.activated.connect(self.open_datepicker)

        self.with_notification = QCheckBox('add notification')
        self.with_notification.clicked.connect(self.set_notification_time)
        self.notification_time = QTimeEdit()
        self.notification_time.hide()

        second_layout = QHBoxLayout()
        second_layout.addWidget(self.date_choice)
        second_layout.addWidget(self.with_notification)
        second_layout.addWidget(self.notification_time)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.confirm_button)

        main_layout.addLayout(text_layout)
        main_layout.addLayout(second_layout)
        main_layout.addLayout(button_layout)

    def set_notification_time(self):
        if self.with_notification.isChecked():
            self.notification_time.show()
        else:
            self.notification_time.hide()

    def closeDialog(self):
        self.close()

    def open_datepicker(self):
        if self.date_choice.currentIndex() == 0:
            self.picked_date = datetime.now().date()
        elif self.date_choice.currentIndex() == 1:
            self.picked_date = (datetime.now() + timedelta(days=1)).date()
        if self.date_choice.currentIndex() == 2:
            self.dateedit = DateChoiceDialog(self)
            self.dateedit.show()

    def change_combobox_option(self, picked_date):
        # changing the content
        self.date_choice.setItemText(2, picked_date)

    def _enforce_summary_not_empty(self):
        if len(self.summary_line_edit.text()
               ) > 0 and not self.confirm_button.isEnabled():
            self.confirm_button.setEnabled(True)
        elif len(self.summary_line_edit.text()) == 0:
            self.confirm_button.setEnabled(False)

    def _get_default_datetime(self) -> QDateTime:
        dt = QDateTime.currentDateTime().addSecs(60 * 60)
        return dt.addSecs(-dt.time().second()).addMSecs(-dt.time().msec())

    def set_picked_date(self, picked_date: date):
        self.picked_date = picked_date


class DateChoiceDialog(QDialog):
    def __init__(self, parent=None):
        super(DateChoiceDialog, self).__init__(parent)
        self.parent = parent

        main_layout = QVBoxLayout()
        self.calendar = QCalendarWidget()
        main_layout.addWidget(self.calendar)
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton('Save')
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.setAutoDefault(False)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.save_btn)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        self.cancel_btn.clicked.connect(self.closeDialog)
        self.save_btn.clicked.connect(self.saveDate)

    def closeDialog(self):
        self.close()

    def saveDate(self):
        qdate_obj = self.calendar.selectedDate()
        picked_date_str = qdate_obj.toString()  # Преобразуем QDate в строку
        picked_date_date = date(qdate_obj.year(), qdate_obj.month(), qdate_obj.day())
        self.parent.set_picked_date(picked_date_date)
        self.parent.change_combobox_option(picked_date_str)
        self.closeDialog()
