import os
import json
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog

CONFIG_FILE = os.path.expanduser("~/.arxiv-workflow/config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set API Keys & Settings")

        self.layout = QVBoxLayout()

        # Notion Token
        self.notion_label = QLabel("Notion Token:")
        self.notion_input = QLineEdit()
        self.layout.addWidget(self.notion_label)
        self.layout.addWidget(self.notion_input)

        # Notion Database ID
        self.database_id_label = QLabel("Notion Database ID:")
        self.database_id_input = QLineEdit()
        self.layout.addWidget(self.database_id_label)
        self.layout.addWidget(self.database_id_input)

        # Semantic Scholar Key
        self.ss_key_label = QLabel("Semantic Scholar Key:")
        self.ss_key_input = QLineEdit()
        self.layout.addWidget(self.ss_key_label)
        self.layout.addWidget(self.ss_key_input)

        # Semantic Scholar Sleep Interval
        self.ss_sleep_label = QLabel("SS Sleep Interval (seconds):")
        self.ss_sleep_input = QLineEdit()
        self.layout.addWidget(self.ss_sleep_label)
        self.layout.addWidget(self.ss_sleep_input)

        # Download Directory
        self.download_dir_label = QLabel("Download Directory:")
        self.download_dir_input = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.select_download_directory)

        download_dir_layout = QHBoxLayout()
        download_dir_layout.addWidget(self.download_dir_input)
        download_dir_layout.addWidget(self.browse_button)
        self.layout.addWidget(self.download_dir_label)
        self.layout.addLayout(download_dir_layout)

        # Load existing values
        self.load_existing_config()

        # Save + Close Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_config)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.close_button)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

    def load_existing_config(self):
        config = load_config()
        self.notion_input.setText(config.get("notion_token", ""))
        self.database_id_input.setText(config.get("notion_database_id", ""))
        self.ss_key_input.setText(config.get("ss_key", ""))
        self.ss_sleep_input.setText(str(config.get("ss_sleep_interval", 3)))
        self.download_dir_input.setText(config.get("download_dir", "./papers/"))

    def save_config(self):
        config = {
            "notion_token": self.notion_input.text(),
            "notion_database_id": self.database_id_input.text(),
            "ss_key": self.ss_key_input.text(),
            "ss_sleep_interval": float(self.ss_sleep_input.text() or 1),
            "download_dir": self.download_dir_input.text(),
        }
        save_config(config)

        # Optional: update main window's cached config if needed
        if self.parent():
            self.parent().config = config

        self.close()

    def select_download_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        if directory:
            self.download_dir_input.setText(directory)
