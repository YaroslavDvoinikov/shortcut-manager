from threading import Thread

from PyQt6.QtGui import QGuiApplication
from pynput import keyboard
from PySide6 import QtWidgets
from PySide6.QtCore import QObject
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFileDialog

from src.keynormalize import format_keys
from src.shortcut import Shortcut
from src.shortcuts import Shortcuts


class KeyPressFilter(QObject):
    def __init__(self, widget, parent=None):
        super().__init__(parent)
        self.current_keys = set()
        self.widget = widget
        self.is_active = True

        self.listener = keyboard.Listener(
            on_press=self.on_press_pynput, on_release=self.on_release_pynput
        )
        self.listener_thread = Thread(target=self.listener.run, daemon=True)
        self.listener_thread.start()

    def on_press_pynput(self, key):
        if not self.is_active:
            return
        self.current_keys.add(key)
        self.update_ui()

    def on_release_pynput(self, key):
        if key in self.current_keys:
            self.current_keys.discard(key)
        self.update_ui()

    def update_ui(self):
        if not self.is_active:
            return
        try:
            text = format_keys(self.current_keys)
            self.widget.setText(text)
        except RuntimeError:
            self.stop()

    def get_current_keys(self):
        return frozenset(self.current_keys)

    def stop(self):
        self.is_active = False
        if self.listener:
            self.listener.stop()


class KeyCombinationDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Press a key combination")
        self.key_combination = None
        self.text = None
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

        self.eventFilter = KeyPressFilter(self.key_sequence_input, parent=self)

    def save_key_combination(self):
        self.text = self.key_sequence_input.text()
        self.key_combination = self.eventFilter.get_current_keys()
        if self.key_combination:
            self.accept()
        else:
            self.reject()

    def get_key_combination(self):
        return self.key_combination

    def get_text(self):
        return self.text

    def closeEvent(self, event):
        self.eventFilter.stop()
        super().closeEvent(event)

    def accept(self):
        self.eventFilter.stop()
        super().accept()

    def reject(self):
        self.eventFilter.stop()
        super().reject()


class CreateShortcutDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shortcut_data = Shortcuts().get_shortcuts()

        self.setWindowTitle("Create Shortcut")
        self.selected_command = None
        self.key_combination = None
        self.optional_arguments = []
        self.can_accept = True

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

        self.start_screen_record_btn = QtWidgets.QPushButton("Start screen recording")
        self.start_screen_record_btn.setCheckable(True)
        self.start_screen_record_btn.setMaximumWidth(200)

        self.power_off_btn = QtWidgets.QPushButton("Power off")
        self.power_off_btn.setCheckable(True)
        self.power_off_btn.setMaximumWidth(200)

        self.reboot_btn = QtWidgets.QPushButton("Reboot")
        self.reboot_btn.setCheckable(True)
        self.reboot_btn.setMaximumWidth(200)

        self.logout_btn = QtWidgets.QPushButton("Logout")
        self.logout_btn.setCheckable(True)
        self.logout_btn.setMaximumWidth(200)

        self.start_audio_record_btn = QtWidgets.QPushButton("Start audio recording")
        self.start_audio_record_btn.setCheckable(True)
        self.start_audio_record_btn.setMaximumWidth(200)

        # Add Future buttons HERE ------------------------------------------------------------
        self.command_button_group.addButton(self.run_executable_btn, 0)
        self.command_button_group.addButton(self.screenshot_btn, 1)
        self.command_button_group.addButton(self.start_screen_record_btn, 2)
        self.command_button_group.addButton(self.power_off_btn, 3)
        self.command_button_group.addButton(self.reboot_btn, 4)
        self.command_button_group.addButton(self.logout_btn, 5)
        self.command_button_group.addButton(self.start_audio_record_btn, 6)

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
        command_buttons_layout.addWidget(self.start_screen_record_btn, 0, 2)
        command_buttons_layout.addWidget(self.power_off_btn, 1, 0)
        command_buttons_layout.addWidget(self.reboot_btn, 1, 1)
        command_buttons_layout.addWidget(self.logout_btn, 1, 2)
        command_buttons_layout.addWidget(self.start_audio_record_btn, 2, 0)

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

        if not self.can_accept:
            self.error_label.setText(
                "Missing required parameters for selected command!"
            )
            return

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
            temp_combo = format_keys(self.key_combination)
            for shortcut in Shortcuts().get_shortcuts().values():
                if shortcut.combination == temp_combo:
                    self.error_label.setText(
                        "Shortcut with this key combination already exists!"
                    )
                    return

        if self.selected_command is None:
            self.error_label.setText("Command must be selected!")
            return

        self.accept()

    def on_command_selected(self, button):
        # Switch case to all selected commands, to get optional arguments
        self.optional_arguments.clear()
        self.selected_command = self.command_button_group.id(button)
        match self.selected_command:
            case 0:
                file = QFileDialog.getOpenFileName(self, caption="Choose an executable")
                if file[0] != "":
                    self.optional_arguments.append(file[0])
                    self.can_accept = True
                    self.run_executable_btn.setText(file[0])
                else:
                    self.can_accept = False
                    self.run_executable_btn.setText("Run an executable")
            case 1:
                dir = QFileDialog.getExistingDirectory(
                    self, caption="Choose a directory where to save the screenshots"
                )
                if dir != "":
                    self.optional_arguments.append(dir)
                    self.can_accept = True
                else:
                    self.can_accept = False
            case 2:
                dir = QFileDialog.getExistingDirectory(
                    self, caption="Choose a directory where to save the screenshots"
                )
                if dir != "":
                    self.optional_arguments.append(dir)
                    self.can_accept = True
                    width, height = QGuiApplication.primaryScreen().size().toTuple()
                    self.optional_arguments.append(width)
                    self.optional_arguments.append(height)
                else:
                    self.can_accept = False
            case 6:
                dir = QFileDialog.getExistingDirectory(
                    self, caption="Choose a directory where to save the screenshots"
                )
                if dir != "":
                    self.optional_arguments.append(dir)
                    self.can_accept = True
                else:
                    self.can_accept = False
            case _:
                self.can_accept = True

    def open_key_combination_dialog(self):
        create_shortcut_window = KeyCombinationDialog(self)
        result = create_shortcut_window.exec()
        if result == QtWidgets.QDialog.Accepted:
            self.key_combination = create_shortcut_window.get_key_combination()
            text = create_shortcut_window.get_text()
            self.combination_input_button.setText(text)

    def get_data(self) -> Shortcut:
        name = self.name_input.text().strip()
        key_combination = format_keys(self.key_combination)
        selected_command = self.selected_command
        description = self.description_input.text().strip()
        if len(self.optional_arguments) != 0:
            return Shortcut(
                [
                    name,
                    key_combination,
                    selected_command,
                    description,
                    self.optional_arguments,
                ]
            )
        else:
            return Shortcut(
                [
                    name,
                    key_combination,
                    selected_command,
                    description,
                    [],
                ]
            )
