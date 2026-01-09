from PySide6 import QtWidgets
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMenu, QSystemTrayIcon

from src.actions import info, stop_recording
from src.createshortcutdialog import CreateShortcutDialog
from src.globallistener import GlobalListener
from src.settingsdialog import SettingsDialog
from src.shortcutdialog import ShortcutDialog
from src.shortcuts import Shortcuts


class MainWindow(QtWidgets.QListWidget):
    def __init__(self):
        super().__init__()
        self.__shortcuts = Shortcuts()
        self.setWindowTitle("Shortcut Manager")

        # App tray
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon("icon.png"))
        self.tray.setToolTip("Shortcut Manager")

        tray_menu = QMenu()

        show_action = QAction("Show", self)
        exit_action = QAction("Close", self)

        show_action.triggered.connect(self.show_window)
        exit_action.triggered.connect(self.exit_app)

        tray_menu.addAction(show_action)
        tray_menu.addAction(exit_action)

        self.tray.setContextMenu(tray_menu)
        self.tray.activated.connect(self.on_tray_activated)
        self.tray.show()

        self.open_settings_button = QtWidgets.QPushButton("Settings")
        self.open_settings_button.clicked.connect(self.open_settings)
        self.create_new_shortcut = QtWidgets.QPushButton("Create shortcut")
        self.create_new_shortcut.clicked.connect(self.open_create_shortcut_window)

        # Table with shortcuts
        self.shortcut_table = QtWidgets.QTableWidget()
        self.shortcut_table.cellDoubleClicked.connect(self.open_shortcut_dialog)
        self.shortcut_table.setColumnCount(3)
        self.shortcut_table.setHorizontalHeaderLabels(["Name", "Combination", "Action"])
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

    # Rewriting virtual method, so the app is only hidden when the user clicks the close button
    def closeEvent(self, event):
        event.ignore()
        self.hide()

    # Method for show button in trey
    def show_window(self):
        self.show()
        self.raise_()
        self.activateWindow()

    # Showing app window when tray icon is clicked
    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show_window()

    # Completely exiting the app when the user clicks the close button in tray
    def exit_app(self):
        self.tray.hide()
        stop_recording()
        QtWidgets.QApplication.quit()

    def open_shortcut_dialog(self, row, column):
        combination = self.shortcut_table.item(row, 1).text()

        dialog = ShortcutDialog(self, combination)
        dialog.resize(400, 200)
        result = dialog.exec()
        if result == QtWidgets.QDialog.Accepted:
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
                row_pos, 1, QtWidgets.QTableWidgetItem(shortcut.combination)
            )
            self.shortcut_table.setItem(
                row_pos, 2, QtWidgets.QTableWidgetItem(info(shortcut.command))
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
                row_pos, 1, QtWidgets.QTableWidgetItem(shortcut_to_add.combination)
            )
            self.shortcut_table.setItem(
                row_pos, 2, QtWidgets.QTableWidgetItem(info(shortcut_to_add.command))
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
            self.__shortcuts.add(shortcut)
            self.__shortcuts.save_shortcuts_file("shortcuts.csv")
            self.update_shortcut_table(shortcut_to_add=shortcut)
            GlobalListener().reload_shortcuts()
