from PySide6 import QtWidgets
from PySide6.QtGui import QKeySequence

from src.createshortcutdialog import CreateShortcutDialog
from src.global_listener import GlobalListener
from src.settingsdialog import SettingsDialog
from src.shortcut import Shortcut, command_id_to_class
from src.shortcuts import Shortcuts


class MainWindow(QtWidgets.QListWidget):
    def __init__(self):
        super().__init__()
        self.__shortcuts = Shortcuts()
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

        self.create_shortcut_table()

    def open_settings(self):
        settings = SettingsDialog(self)
        settings.exec()

    def create_shortcut_table(self):
        self.shortcut_table.setRowCount(0)
        for shortcut in self.__shortcuts.get_shortcuts().values():
            row_pos = self.shortcut_table.rowCount()
            self.shortcut_table.insertRow(row_pos)
            self.shortcut_table.setItem(
                row_pos, 0, QtWidgets.QTableWidgetItem(shortcut.name)
            )
            self.shortcut_table.setItem(
                row_pos,
                1,
                QtWidgets.QTableWidgetItem(shortcut.combination),
            )
            self.shortcut_table.setItem(
                row_pos,
                2,
                QtWidgets.QTableWidgetItem(
                    command_id_to_class[shortcut.command].info()
                ),
            )
            self.shortcut_table.setItem(
                row_pos, 3, QtWidgets.QTableWidgetItem(shortcut.description)
            )
        self.shortcut_table.resizeColumnsToContents()

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
                QtWidgets.QTableWidgetItem(shortcut_to_add.combination),
            )
            self.shortcut_table.setItem(
                row_pos,
                2,
                QtWidgets.QTableWidgetItem(
                    command_id_to_class[shortcut_to_add.command].info()
                ),
            )
            self.shortcut_table.setItem(
                row_pos, 3, QtWidgets.QTableWidgetItem(shortcut_to_add.description)
            )
        if shortcut_to_delete:
            self.create_shortcut_table()

        self.shortcut_table.resizeColumnsToContents()

    def open_create_shortcut_window(self):
        create_shortcut_window = CreateShortcutDialog(parent=self)
        create_shortcut_window.resize(600, 400)
        result = create_shortcut_window.exec()
        if result == QtWidgets.QDialog.Accepted:
            shortcut = create_shortcut_window.get_data()
            self.update_shortcut_table(shortcut_to_add=shortcut)
            self.__shortcuts.update_shortcuts_file(shortcut_to_add=shortcut)
            GlobalListener().reload_shortcuts()
