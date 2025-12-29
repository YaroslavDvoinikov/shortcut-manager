from imaplib import Commands

from PySide6 import QtWidgets
from PySide6.QtCore import QEvent, QKeyCombination, QObject
from PySide6.QtGui import QKeySequence, Qt

from src.shortcut import Shortcut
from src.shortcuts import Shortcuts


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


class CreateShortcutDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shortcut_data = Shortcuts().get_shortcuts()

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
        else:
            for shortcut in Shortcuts().get_shortcuts().values():
                if shortcut.combination == self.key_combination.toCombined():
                    self.error_label.setText(
                        "Shortcut with this key combination already exists!"
                    )
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
        key_combination = self.key_combination.toCombined()
        selected_command = self.selected_command
        description = self.description_input.text().strip()
        return Shortcut([name, key_combination, selected_command, description])
