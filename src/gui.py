from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
import os
import sys

os.environ.pop('QT_STYLE_OVERRIDE', None)

class SettingsWindow(QtWidgets.QDialog):
    def __init__(self,parent):
        super().__init__(parent)

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

        self.import_settings_button = QtWidgets.QPushButton("Import Settings")
        self.export_settings_button = QtWidgets.QPushButton("Export Settings")

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.theme_label)
        main_layout.addWidget(self.theme_group)
        main_layout.addWidget(self.import_settings_button)
        main_layout.addWidget(self.export_settings_button)





class MainWindow(QtWidgets.QListWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shortcut Manager")

        self.open_settings_button = QtWidgets.QPushButton("Settings")
        self.open_settings_button.clicked.connect(self.open_settings)
        self.create_new_shortcut = QtWidgets.QPushButton("Create shortcut")
        self.create_new_shortcut.clicked.connect(self.test_add_shortcut)

        #Table with shortcuts
        self.shortcut_table = QtWidgets.QTableWidget()
        self.shortcut_table.setColumnCount(5)
        self.shortcut_table.setHorizontalHeaderLabels(["Name","Combination","Description","Edit","Delete"])
        self.shortcut_table.resizeColumnsToContents()
        self.shortcut_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)


        #Layout of an application
        main_layout = QtWidgets.QVBoxLayout(self)

        waybar_layout = QtWidgets.QHBoxLayout()
        waybar_layout.addWidget(self.open_settings_button)
        waybar_layout.addWidget(self.create_new_shortcut)

        main_layout.addLayout(waybar_layout)
        main_layout.addWidget(self.shortcut_table)

    def test_add_shortcut(self):
        row_pos = self.shortcut_table.rowCount()
        self.shortcut_table.insertRow(row_pos)
        self.shortcut_table.setItem(row_pos, 0, QtWidgets.QTableWidgetItem("Run GoogleChrome"))
        self.shortcut_table.setItem(row_pos, 1, QtWidgets.QTableWidgetItem("Ctrl+X"))
        self.shortcut_table.setItem(row_pos, 2, QtWidgets.QTableWidgetItem("Runs a new GoogleChrome instance"))
        self.shortcut_table.setItem(row_pos, 3, QtWidgets.QTableWidgetItem("Edit"))
        self.shortcut_table.setItem(row_pos, 4, QtWidgets.QTableWidgetItem("Delete"))
        self.shortcut_table.resizeColumnsToContents()

    def open_settings(self):
        settings = SettingsWindow(self)
        settings.exec()


def run():
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec())
