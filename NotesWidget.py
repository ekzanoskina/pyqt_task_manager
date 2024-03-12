
from random import choice

from PyQt6 import uic
from PyQt6.QtWidgets import QWidget

from Note import Note

class NoteItem(QWidget):
    def __init__(self, note: Note):
        super().__init__()
        self.ui = uic.loadUi('note.ui', self)
        self.ui.note_summary.setReadOnly(True)
        self.ui.note_summary.setText(note.summary)


class NotesWidget(QWidget):
    def __init__(self, db, parent=None):
        super(NotesWidget, self).__init__(parent)
        self._db = db
        self.ui = uic.loadUi("NotesWidget.ui", self)
        self.ui.add_note_btn.clicked.connect(self.create_note)
        self.show_notes()


    def create_note(self):
        summary = self.ui.note_line_edit.text()
        note = Note(summary)
        self._db.save_note(note)
        self.show_notes()

    def show_notes(self):
        colors_list = ['#90B9D5', '#9BAEBC', '#D0A8C1', '#BAA6B2']
        notes_list = self._db.get_notes()
        row = 0
        column = 0
        for i in range(len(notes_list)):
            if column == 3:
                column = 0
                row += 1
            note_item = NoteItem(notes_list[i])
            note_item.setStyleSheet("""#note_item_2 {{background-color: {color}}}""".format(color=choice(colors_list)))
            self.ui.notes_grid_layout.addWidget(note_item, row, column)

            column += 1
