from PySide6.QtCore import QKeyCombination
from PySide6.QtGui import QKeySequence


class Shortcut:
    def __init__(self, data: list):
        self.name = data[0]
        self.combination = int(data[1])
        self.command = int(data[2])
        self.description = data[3]

    def readable_key_sequence(self):
        kc = QKeyCombination.fromCombined(self.combination)
        return QKeySequence(kc).toString()

    def get_key_combination(self):
        return QKeyCombination.fromCombined(self.combination)

    def __str__(self):
        return f"\n Name: {self.name}\n Combination: {self.combination}\n Command: {self.command}\n Description: {self.description}\n"
