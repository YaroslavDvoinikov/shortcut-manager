from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog

from settings import Settings


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.__settings = Settings()

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
        if self.__settings.get_setting('theme') == 'light':
            self.dark_radio.setChecked(False)
            self.light_radio.setChecked(True)
        else:
            self.dark_radio.setChecked(True)
            self.light_radio.setChecked(False)

        def set_light(checked: bool):
            if checked:
                self.__settings.set_setting('theme', 'light')
        def set_dark(checked: bool):
            if checked:
                self.__settings.set_setting('theme', 'dark')
        self.light_radio.toggled.connect(set_light)
        self.dark_radio.toggled.connect(set_dark)

        self.import_settings_button = QtWidgets.QPushButton("Import Settings")
        def on_click_import_settings():
            file = QFileDialog.getOpenFileName(self, caption="Select settings", filter="Setting Files (*.json)")
            if file[0] != "":
                self.__settings.replace_settings_file(file[0])
                if self.__settings.get_setting('theme') == 'light':
                    self.dark_radio.setChecked(False)
                    self.light_radio.setChecked(True)
                else:
                    self.dark_radio.setChecked(True)
                    self.light_radio.setChecked(False)
        self.import_settings_button.clicked.connect(on_click_import_settings)
        self.export_settings_button = QtWidgets.QPushButton("Export Settings")
        def on_click_export_settings():
            file = QFileDialog.getOpenFileName(self, caption="Select settings", filter="Setting Files (*.json)")
            print(file)
            if file[0] != "":
                self.__settings.save_settings_file(file[0])
        self.export_settings_button.clicked.connect(on_click_export_settings)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.theme_label)
        main_layout.addWidget(self.theme_group)
        main_layout.addWidget(self.import_settings_button)
        main_layout.addWidget(self.export_settings_button)
