from PySide6 import QtWidgets

from src.shortcuts import Shortcuts


class ShortcutDialog(QtWidgets.QDialog):
    def __init__(self, parent, combination):
        super().__init__(parent)
        self.__shortcuts = Shortcuts()
        self.__shortcut = self.__shortcuts.get_shortcuts()[combination]

        self.setWindowTitle("Edit Shortcut")

        self.name_title = QtWidgets.QLabel("Name of a shortcut:")
        self.name_input = QtWidgets.QLineEdit(text=self.__shortcut.name)
        self.name_input.setPlaceholderText("Enter name")

        self.delete_button = QtWidgets.QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_shortcut)
        self.delete_button.setStyleSheet("color: red;")

        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.clicked.connect(self.close_dialog)
        self.save_button.setStyleSheet("color: green;")

        main_layout = QtWidgets.QVBoxLayout(self)

        main_layout.addWidget(self.name_title)
        main_layout.addWidget(self.name_input)
        main_layout.addWidget(self.save_button)
        main_layout.addWidget(self.delete_button)

    def delete_shortcut(self):
        self.__shortcuts.remove(self.__shortcut.combination)
        self.__shortcuts.save_shortcuts_file("shortcuts.csv")
        self.accept()

    def close_dialog(self):
        self.__shortcut.name = self.name_input.text()
        self.__shortcuts.update(self.__shortcut.combination, self.__shortcut)
        self.__shortcuts.save_shortcuts_file("shortcuts.csv")
        self.accept()
