import sys
import os
import json
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel
from PyQt5 import uic
#from PyQt5.QtCore import Qt

from main2 import auto_fetch_workflow
from config_dialog import ConfigDialog

CONFIG_FILE = os.path.expanduser("~/.paper-database-to-notion/config.json")
os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

# pyinstaller --noconsole --name "ArxivWorkflow" --add-data "arxiv.ui:." QtUI.py


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("arxiv.ui", self)

        # Connect the main button
        self.searchButton.clicked.connect(self.call_function)

        # Add help labels for hover help
        self.hoverLabels = {}

        self.add_hover_help(self.entry1, "Paper identifier (DOI, arXiv link, Semantic Scholar link)")
        self.add_hover_help(self.entry2, "Subfolder where this paper will be downloaded.")
        self.add_hover_help(self.tagsEntry, "Tags for this paper, separated by commas or semicolons.")

        # Add the "Configurations" menu action connection
        self.actionOpenConfig.triggered.connect(self.open_config_window)

        # Load config
        self.config = load_config()

    def add_hover_help(self, widget, help_text):
        """ Adds a floating hover label for a given widget. """
        label = QLabel(help_text, self)
        label.setStyleSheet("""
            background-color: #3c3f41;
            color: white;
            border: 1px solid black;
            padding: 5px;
            font-size: 14pt;
        """)
        label.hide()

        self.hoverLabels[widget] = label
        widget.installEventFilter(self)

    def eventFilter(self, source, event):
        if source in self.hoverLabels:
            if event.type() == event.Enter:
                self.show_hover_help(source)
            elif event.type() == event.Leave:
                self.hoverLabels[source].hide()
        return super().eventFilter(source, event)

    def show_hover_help(self, widget):
        label = self.hoverLabels[widget]
        label.adjustSize()

        pos = widget.mapToGlobal(widget.rect().bottomLeft())
        pos = self.mapFromGlobal(pos)

        if pos.x() + label.width() > self.width():
            pos.setX(self.width() - label.width() - 10)
        if pos.y() + label.height() > self.height():
            pos.setY(self.height() - label.height() - 10)

        label.move(pos)
        label.show()

    def call_function(self):
        query = {
            "query":self.entry1.text().strip(),
            "project": self.entry2.text().strip() or "uncategorized",
            "tags": [tag.strip() for tag in re.split(r'[;,]', self.tagsEntry.text().strip()) if tag.strip()]
        }


        # Check for missing Notion credentials
        notion_token = self.config.get("notion_token", "").strip()
        notion_database_id = self.config.get("notion_database_id", "").strip()

        if not notion_token or not notion_database_id:
            QMessageBox.critical(self, "Missing Configuration", 
                "Notion Token and Notion Database ID must be set before searching and downloading.")
            return

        # Call your existing workflow function
        result = auto_fetch_workflow(query)
        QMessageBox.information(self, "Status", result)

        self.entry1.clear()
        self.entry2.clear()
        self.tagsEntry.clear()


    def open_config_window(self):
        self.config_dialog = ConfigDialog(self)
        self.config_dialog.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
