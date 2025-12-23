import os
import sys
from pydoc import describe
from this import s

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QKeySequence

os.environ.pop("QT_STYLE_OVERRIDE", None)
os.environ["QT_LOGGING_RULES"] = "qt.qpa.wayland.textinput=false"


command_id_to_name = {0: "Run an executable", 1: "Take screenshot"}


class Shortcut:
    def __init__(self, data: list):
        self.name = data[0]
        self.combination = data[1]
        self.command = data[2]
        self.description = data[3]

    def __str__(self):
        return f"\n Name: {self.name}\n Combination: {self.combination}\n Command: {self.command}\n Description: {self.description}\n"


# Key listener class
class KeyPressFilter(QObject):
    MODIFIER_KEYS = {
        Qt.Key_Control,
        Qt.Key_Shift,
        Qt.Key_Alt,
        Qt.Key_Meta,
    }

    def eventFilter(self, widget, event):
        # To avoid showing only modifier keys pressed
        if event.type() == QEvent.KeyPress:
            if event.key() in self.MODIFIER_KEYS:
                return True

            combo = event.keyCombination()
            text = QKeySequence(combo).toString()

            widget.key_sequence_input.setText(text)
            widget.key_combination = combo
            return True
        return False


class KeyCombinationDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Press a key combination")
        self.key_combination = None

        self.key_sequence_label = QtWidgets.QLabel("Press a key combination:")
        self.key_sequence_label.setAlignment(Qt.AlignCenter)

        self.key_sequence_input = QtWidgets.QLineEdit()
        self.key_sequence_input.setReadOnly(True)
        self.key_sequence_input.setPlaceholderText("Waiting for key combination...")

        self.key_sequence_save_button = QtWidgets.QPushButton("Save")
        self.key_sequence_save_button.clicked.connect(self.save_key_combination)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.key_sequence_label)
        layout.addWidget(self.key_sequence_input)
        layout.addWidget(self.key_sequence_save_button)
        self.setLayout(layout)

        self.eventFilter = KeyPressFilter(parent=self)
        self.installEventFilter(self.eventFilter)

    def save_key_combination(self):
        if self.key_combination:
            self.accept()
        else:
            self.reject()

    def get_key_combination(self):
        return self.key_combination


class CreateShortcutWindow(QtWidgets.QDialog):
    def __init__(self, shortcut_data, parent=None):
        super().__init__(parent)
        self.shortcut_data = shortcut_data

        self.setWindowTitle("Create Shortcut")
        self.selected_command = None
        self.key_combination = None

        # Name input
        self.name_title = QtWidgets.QLabel("Name of a shortcut:")
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Enter name")

        # Combination input
        self.combination_title = QtWidgets.QLabel("Key combination:")
        self.combination_input_button = QtWidgets.QPushButton(
            "Press to input a key combination"
        )
        self.combination_input_button.clicked.connect(self.open_key_combination_dialog)

        # Command input group
        self.command_title = QtWidgets.QLabel("Command:")
        self.command_button_group = QtWidgets.QButtonGroup(self)
        self.command_button_group.setExclusive(True)

        # Run an executable button
        self.run_executable_btn = QtWidgets.QPushButton("Run an executable")
        self.run_executable_btn.setCheckable(True)
        self.run_executable_btn.setMaximumWidth(200)

        # Take screenshot button
        self.screenshot_btn = QtWidgets.QPushButton("Take screenshot")
        self.screenshot_btn.setCheckable(True)
        self.screenshot_btn.setMaximumWidth(200)

        # Add Future buttons HERE ------------------------------------------------------------
        self.command_button_group.addButton(self.run_executable_btn, 0)
        self.command_button_group.addButton(self.screenshot_btn, 1)

        self.command_button_group.buttonClicked.connect(self.on_command_selected)

        # Description input
        self.description_title = QtWidgets.QLabel("Description of a shortcut:")
        self.description_input = QtWidgets.QLineEdit()
        self.description_input.setPlaceholderText("Enter description")

        # Error label
        self.error_label = QtWidgets.QLabel("")
        self.error_label.setStyleSheet("color: red;")

        # Create button
        self.create_button = QtWidgets.QPushButton("Create")
        self.create_button.clicked.connect(self.validate)

        # Add future buttons HERE to layout! ----------------------------
        command_buttons_layout = QtWidgets.QGridLayout()
        command_buttons_layout.addWidget(self.run_executable_btn, 0, 0)
        command_buttons_layout.addWidget(self.screenshot_btn, 0, 1)

        main_layout = QtWidgets.QVBoxLayout(self)

        main_layout.addWidget(self.name_title)
        main_layout.addWidget(self.name_input)
        main_layout.addWidget(self.combination_title)
        main_layout.addWidget(self.combination_input_button)
        main_layout.addWidget(self.command_title)
        main_layout.addLayout(command_buttons_layout)
        main_layout.addWidget(self.description_title)
        main_layout.addWidget(self.description_input)
        main_layout.addStretch()
        main_layout.addWidget(self.error_label)
        main_layout.addWidget(self.create_button)

    # validating all fields
    def validate(self):
        name = self.name_input.text().strip()

        if not name:
            self.error_label.setText("Name must be filled!")
            return

        if name in self.shortcut_data:
            self.error_label.setText("Shortcut with this name already exists!")
            return

        if self.key_combination is None:
            self.error_label.setText("Key combination must be selected!")
            return

        if self.selected_command is None:
            self.error_label.setText("Command must be selected!")
            return

        self.accept()

    def on_command_selected(self, button):
        self.selected_command = self.command_button_group.id(button)

    def open_key_combination_dialog(self):
        create_shortcut_window = KeyCombinationDialog(self)
        result = create_shortcut_window.exec()
        if result == QtWidgets.QDialog.Accepted:
            self.key_combination = create_shortcut_window.get_key_combination()
            text = QKeySequence(self.key_combination).toString()
            self.combination_input_button.setText(text)

    def get_data(self) -> Shortcut:
        name = self.name_input.text().strip()
        key_combination = self.key_combination
        selected_command = self.selected_command
        description = self.description_input.text().strip()
        return Shortcut([name, key_combination, selected_command, description])


class SettingsWindow(QtWidgets.QDialog):
    def __init__(self, parent):
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
        settings = SettingsWindow(self)
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
        create_shortcut_window = CreateShortcutWindow(self.shortcut_data, parent=self)
        create_shortcut_window.resize(600, 400)
        result = create_shortcut_window.exec()
        if result == QtWidgets.QDialog.Accepted:
            shortcut = create_shortcut_window.get_data()
            self.shortcut_data[shortcut.name] = shortcut
            self.update_shortcut_table(shortcut_to_add=shortcut)
            self.update_shortcut_file(shortcut_to_add=shortcut)
            print(shortcut)


def run():
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec())
