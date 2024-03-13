from functools import partial
from random import choice

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.uic.properties import QtCore

from Note import Note

class NoteItem(QWidget):
    save = pyqtSignal(Note)
    delete = pyqtSignal(Note)
    def __init__(self, note: Note):
        super().__init__()
        self.ui = uic.loadUi('Note.ui', self)
        self.note = note
        self.ui.note_summary.setReadOnly(True)
        self.ui.note_summary.setText(note.summary)
        self.ui.edit_btn.clicked.connect(self.edit_note)
        self.ui.delete_btn.clicked.connect(self.delete_note)

    def handle_focus_changed(self, old_widget, now_widget):
        """Saves a note if the focus changes"""
        if self.ui.note_summary is old_widget:
            self.note.summary = self.ui.note_summary.toPlainText()
            self.save.emit(self.note)
            self.ui.note_summary.setReadOnly(True)


    def edit_note(self):
        """Makes a note widget editable"""
        self.ui.note_summary.setReadOnly(False)
        QApplication.instance().focusChanged.connect(self.handle_focus_changed)

    def delete_note(self):
        self.delete.emit(self.note)

class NotesWidget(QWidget):
    def __init__(self, db, parent=None):
        super(NotesWidget, self).__init__(parent)
        self._db = db
        self.ui = uic.loadUi("NotesWidget.ui", self)
        self.ui.add_note_btn.clicked.connect(self.create_note)
        self.positions = {}
        self.show_notes()



    def create_note(self):
        summary = self.ui.note_line_edit.text()
        self.ui.note_line_edit.setText('')
        note = Note(summary)
        self._db.save_note(note)
        self.show_notes()


    def show_notes(self):
        notes_list = self._db.get_notes()
        row = 0
        column = 0
        for i in range(len(notes_list)):
            if column == 3:
                column = 0
                row += 1
            note_item = NoteItem(notes_list[i])
            note_item.save.connect(self.save_changes)
            note_item.delete.connect(partial(self.delete_note, note_item=note_item))
            self.paint_note(note_item)
            self.ui.notes_grid_layout.addWidget(note_item, row, column)
            column += 1

    def save_changes(self, note):
        self._db.save_note(note)

    def delete_note(self, note, note_item=None):

        # self.ui.notes_grid_layout.hideWidget(note_item)
        note_item.hide()
        # note_item = None
        self._db.delete_note(note)


    def paint_note(self, note_item):
        """Adds colors to note stickers"""
        colors_list = ['#90B9D5', '#9BAEBC', '#D0A8C1', '#BAA6B2']
        note_item.setStyleSheet("""#note_item_2 {{background-color: {color}}}""".format(color=choice(colors_list)))