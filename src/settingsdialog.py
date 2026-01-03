from ast import Global

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog

from src.global_listener import GlobalListener
from src.settings import Settings
from src.shortcuts import Shortcuts
from src.theme import reload_theme


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.__settings = Settings()
        self.__shortcuts = Shortcuts()
        self.__parent = parent

        self.setWindowTitle("Settings")

        theme_layout = QtWidgets.QHBoxLayout()

        self.theme_label = QtWidgets.QLabel("Theme")
        self.theme_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.theme_group = QtWidgets.QGroupBox()
        self.theme_group.setLayout(theme_layout)

        self.dark_radio = QtWidgets.QRadioButton("Dark")
        theme_layout.addWidget(self.dark_radio)
        self.light_radio = QtWidgets.QRadioButton("Light")
        theme_layout.addWidget(self.light_radio)
        if self.__settings.get_setting("theme") == "light":
            self.dark_radio.setChecked(False)
            self.light_radio.setChecked(True)
        else:
            self.dark_radio.setChecked(True)
            self.light_radio.setChecked(False)

        def set_light(checked: bool):
            if checked:
                self.__settings.set_setting("theme", "light")
                reload_theme()

        def set_dark(checked: bool):
            if checked:
                self.__settings.set_setting("theme", "dark")
                reload_theme()

        self.light_radio.toggled.connect(set_light)
        self.dark_radio.toggled.connect(set_dark)

        self.import_settings_button = QtWidgets.QPushButton("Import Settings")

        def on_click_import_settings():
            file = QFileDialog.getOpenFileName(
                self, caption="Import Settings", filter="Setting Files (*.json)"
            )
            if file[0] != "":
                self.__settings.replace_settings_file(file[0])
                if self.__settings.get_setting("theme") == "light":
                    self.dark_radio.setChecked(False)
                    self.light_radio.setChecked(True)
                else:
                    self.dark_radio.setChecked(True)
                    self.light_radio.setChecked(False)

        self.import_settings_button.clicked.connect(on_click_import_settings)
        self.export_settings_button = QtWidgets.QPushButton("Export Settings")

        def on_click_export_settings():
            file = QFileDialog.getSaveFileName(
                self, caption="Export Settings", filter="Setting Files (*.json)"
            )
            print(file)
            if file[0] != "":
                self.__settings.save_settings_file(file[0])

        self.export_settings_button.clicked.connect(on_click_export_settings)

        self.import_shortcuts_button = QtWidgets.QPushButton("Import Shortcuts")

        def on_click_import_shortcuts():
            file = QFileDialog.getOpenFileName(
                self, caption="Import Shortcuts", filter="Shortcut Files (*.csv)"
            )
            if file[0] != "":
                self.__shortcuts.replace_shortcuts_file(file[0])
                self.__parent.create_shortcut_table()
                GlobalListener().reload_shortcuts()

        self.import_shortcuts_button.clicked.connect(on_click_import_shortcuts)

        self.export_shortcuts_button = QtWidgets.QPushButton("Export Shortcuts")

        def on_click_export_shortcuts():
            file = QFileDialog.getSaveFileName(
                self, caption="Export Shortcuts", filter="Shortcut Files (*.csv)"
            )
            print(file)
            if file[0] != "":
                self.__shortcuts.save_shortcuts_file(file[0])

        self.export_shortcuts_button.clicked.connect(on_click_export_shortcuts)

        settings_layout = QtWidgets.QHBoxLayout()
        settings_layout.addWidget(self.import_settings_button)
        settings_layout.addWidget(self.export_settings_button)

        shortcuts_layout = QtWidgets.QHBoxLayout()
        shortcuts_layout.addWidget(self.import_shortcuts_button)
        shortcuts_layout.addWidget(self.export_shortcuts_button)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.theme_label)
        main_layout.addWidget(self.theme_group)
        main_layout.addLayout(settings_layout)
        main_layout.addLayout(shortcuts_layout)
