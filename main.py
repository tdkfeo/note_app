# main.py
### Imports ###
import json
import sys

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QVBoxLayout, QHBoxLayout, QPushButton,
                             QListWidget, QLabel, QLineEdit, QTextEdit,
                             QGroupBox, QInputDialog)
from PyQt6.QtCore import Qt

import stylesheet

#Dev Tools
from rich import print # Pretty Prints
from rich.traceback import install # Pretty Tracebacks
install(show_locals=True)

### Data ###
notes_data = {}

### Classes ###
class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setup_gui()
        self.event_handlers()

    def setup_gui(self):
        ##? Window Setup
        self.setWindowTitle('Note App')
        self.setGeometry(100, 100, 900, 600)

        ##? Main Tools
        # Note GUI
        self.lbl_notes = QLabel("Notes", self)

        self.lst_notes = QListWidget(self)

        self.btn_create_note = QPushButton("Create", self)
        self.btn_delete_note = QPushButton("Delete", self)

        lyt_note_tools = QHBoxLayout()
        lyt_note_tools.addWidget(self.btn_create_note)
        lyt_note_tools.addWidget(self.btn_delete_note)

        # Tag GUI
        self.lbl_tags = QLabel("Tags", self)

        self.lst_tags = QListWidget(self)

        self.text_search = QLineEdit(self)
        self.text_search.setPlaceholderText("Enter tag...")

        self.btn_create_tag = QPushButton("Create", self)
        self.btn_search_tag = QPushButton("Search", self)
        self.btn_delete_tag = QPushButton("Delete", self)

        lyt_tag_tools = QHBoxLayout()
        lyt_tag_tools.addWidget(self.btn_create_tag)
        lyt_tag_tools.addWidget(self.btn_search_tag)
        lyt_tag_tools.addWidget(self.btn_delete_tag)

        # Main Tools Layout
        lyt_main_tools = QVBoxLayout()
        lyt_main_tools.addWidget(self.lbl_notes)
        lyt_main_tools.addWidget(self.lst_notes)
        lyt_main_tools.addLayout(lyt_note_tools)
        #TODO: Add a line break here
        lyt_main_tools.addWidget(self.lbl_tags)
        lyt_main_tools.addWidget(self.lst_tags)
        lyt_main_tools.addWidget(self.text_search)
        lyt_main_tools.addLayout(lyt_tag_tools)

        ##? Main Text Editor
        # Text GUI
        self.text_editor = QTextEdit(self)

        # Text Editor Layout
        lyt_main_text = QVBoxLayout()
        lyt_main_text.addWidget(self.text_editor)

        ##? Primary Layout
        lyt_main = QHBoxLayout()
        lyt_main.addLayout(lyt_main_text, stretch=2)
        lyt_main.addLayout(lyt_main_tools, stretch=1)

        central_widget = QWidget()
        central_widget.setLayout(lyt_main)
        self.setCentralWidget(central_widget)

    def event_handlers(self):
        self.lst_notes.itemClicked.connect(self.show_note)
        self.text_editor.focusOutEvent = self.save_on_focus_loss
        self.btn_create_note.clicked.connect(self.create_note)
        self.btn_delete_note.clicked.connect(self.delete_note)
        self.btn_create_tag.clicked.connect(self.create_tag)
        self.btn_delete_tag.clicked.connect(self.delete_tag)
        self.btn_search_tag.clicked.connect(self.search_tag)

    def save_on_focus_loss(self, event):
        if self.lst_notes.selectedItems():
            print("Text Editor lost focus")
            note_name = self.lst_notes.selectedItems()[0].text()
            notes[note_name]["text"] = self.text_editor.toPlainText()
            self.write_json()

    def read_json(self):
        with open("notes_data.json", "r") as file:
            temp_data = json.load(file)
        self.lst_notes.addItems(temp_data)
        return temp_data
    
    def write_json(self):
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False, indent=4)

    def show_note(self):
        note_name = self.lst_notes.selectedItems()[0].text()
        self.text_editor.setText(notes[note_name]["text"])
        self.lst_tags.clear()
        self.lst_tags.addItems(notes[note_name]["tags"])

    def create_note(self):
        note_name, state = QInputDialog.getText(main_win, "Create Note", "Name")
        if any(char.isalpha() for char in note_name):
            notes[note_name] = {"text" : "", "tags" : []}
            self.lst_notes.clear()
            self.lst_notes.addItems(notes)
            self.lst_tags.addItems(notes[note_name]["tags"])
            

    def delete_note(self):
        if self.lst_notes.selectedItems():
            note_name = self.lst_notes.selectedItems()[0].text()
            del notes[note_name]
            self.lst_notes.clear()
            self.lst_tags.clear()
            self.text_editor.clear()
            self.lst_notes.addItems(notes)
            self.write_json()

    def create_tag(self): #TODO: Pt2
        if self.lst_notes.selectedItems():
            note_name = self.lst_notes.selectedItems()[0].text()
            tag_name = self.text_search.text()
            #if not tag in notes[key]["tags"]:
            if tag_name not in notes[note_name]["tags"]: #if the tag is not already in the dictionary
                notes[note_name]["tags"].append(tag_name)
                self.lst_tags.addItem(tag_name)
                self.text_search.clear()
                self.write_json()

    def delete_tag(self):
        if self.lst_notes.selectedItems() and self.lst_tags.selectedItems():
            note_name = self.lst_notes.selectedItems()[0].text()
            tag_name = self.lst_tags.selectedItems()[0].text()
            notes[note_name]["tags"].remove(tag_name)
            self.lst_tags.clear()
            self.lst_tags.addItems(notes[note_name]["tags"])
            self.write_json()

    def search_tag(self): #TODO: Pt2
        if self.text_search.text():
            query = self.text_search.text()
            if self.btn_search_tag.text() == "Search" and query:
                notes_filtered = {}
                for note_name in notes:
                    if query in notes[note_name]["tags"]: 
                        notes_filtered[note_name]=notes[note_name]
                self.btn_search_tag.setText("Reset")
                self.lst_notes.clear()
                self.lst_tags.clear()
                self.lst_notes.addItems(notes_filtered)
            elif self.btn_search_tag.text() == "Reset":
                self.text_search.clear()
                self.lst_notes.clear()
                self.lst_tags.clear()
                self.lst_notes.addItems(notes)
                self.btn_search_tag.setText("Search")
            

### App Execution ###
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Windows")
    stylesheet.set_style(app)
    main_win = MainWin()
    main_win.show()
    notes = main_win.read_json()
    sys.exit(app.exec())