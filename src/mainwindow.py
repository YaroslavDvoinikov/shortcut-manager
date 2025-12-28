from PySide6 import QtWidgets
from PySide6.QtGui import QKeySequence

from src.createshortcutdialog import Shortcut, CreateShortcutDialog, command_id_to_name
from src.settingsdialog import SettingsDialog


class MainWindow(QtWidgets.QListWidget):
    def __init__(self):
        super().__init__()
        self.shortcut_data: dict[str, Shortcut] = {}
        self.on_launch()

        self.setWindowTitle("Shortcut Manager")

        self.open_settings_button = QtWidgets.QPushButton("Settings")
        self.open_settings_button.clicked.connect(self.open_settings)
        self.create_new_shortcut = QtWidgets.QPushButton("Create shortcut")
        self.create_new_shortcut.clicked.connect(self.open_create_shortcut_window)

        # Table with shortcuts
        self.shortcut_table = QtWidgets.QTableWidget()
        self.shortcut_table.setColumnCount(4)
        self.shortcut_table.setHorizontalHeaderLabels(
            ["Name", "Combination", "Action", "Description"]
        )
        self.shortcut_table.resizeColumnsToContents()
        self.shortcut_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Layout of an application
        main_layout = QtWidgets.QVBoxLayout(self)

        waybar_layout = QtWidgets.QHBoxLayout()
        waybar_layout.addWidget(self.open_settings_button)
        waybar_layout.addWidget(self.create_new_shortcut)

        main_layout.addLayout(waybar_layout)
        main_layout.addWidget(self.shortcut_table)

    def open_settings(self):
        settings = SettingsDialog(self)
        settings.exec()

    def on_launch(self):
        """Method which launches on the start of application"""
        self.load_shortcuts()
        self.load_settings()
        self.create_shortcut_table()

    def load_settings(self):
        """Loads default settings file, applies settings"""
        pass

    def load_shortcuts(self):
        """Loads default shortcuts file and updates the self.shortcut_data"""
        pass

    def import_settings(self):
        """Import settings from a file, changes content of default settings file"""
        pass

    def export_settings(self):
        """Export settings from default settings file to a created or existing file"""
        pass

    def import_shortcuts(self):
        """Import shortcuts from a file, changes content of default shortcuts file"""
        pass

    def export_shortcuts(self):
        """Export shortcuts from default settings file to a created or existing file"""
        pass

    def update_settings(self, theme=None):
        """Update settings file with new settings, applies settings"""
        pass

    def update_shortcut_file(self, shortcut_to_add=None, shortcut_to_delete=None):
        """Update shortcut file with new shortcuts"""
        pass

    def create_shortcut_table(self):
        """Creates table to view all shortcuts upon launch"""
        pass

    def update_shortcut_table(self, shortcut_to_add=None, shortcut_to_delete=None):
        if shortcut_to_add:
            row_pos = self.shortcut_table.rowCount()
            self.shortcut_table.insertRow(row_pos)
            self.shortcut_table.setItem(
                row_pos, 0, QtWidgets.QTableWidgetItem(shortcut_to_add.name)
            )
            self.shortcut_table.setItem(
                row_pos,
                1,
                QtWidgets.QTableWidgetItem(
                    QKeySequence(shortcut_to_add.combination).toString()
                ),
            )
            self.shortcut_table.setItem(
                row_pos,
                2,
                QtWidgets.QTableWidgetItem(command_id_to_name[shortcut_to_add.command]),
            )
            self.shortcut_table.setItem(
                row_pos, 3, QtWidgets.QTableWidgetItem(shortcut_to_add.description)
            )
        if shortcut_to_delete:
            pass

        self.shortcut_table.resizeColumnsToContents()

    def open_create_shortcut_window(self):
        create_shortcut_window = CreateShortcutDialog(self.shortcut_data, parent=self)
        create_shortcut_window.resize(600, 400)
        result = create_shortcut_window.exec()
        if result == QtWidgets.QDialog.Accepted:
            shortcut = create_shortcut_window.get_data()
            self.shortcut_data[shortcut.name] = shortcut
            self.update_shortcut_table(shortcut_to_add=shortcut)
            self.update_shortcut_file(shortcut_to_add=shortcut)
            print(shortcut)
