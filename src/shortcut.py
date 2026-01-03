import json

from PySide6.QtCore import QKeyCombination
from PySide6.QtGui import QKeySequence

from src.key_normalize import format_keys, normalize_key
from src.run_an_executable import RunAnExecutable
from src.screenshot_taker import ScreenshotTaker

command_id_to_class = {0: RunAnExecutable, 1: ScreenshotTaker}


class Shortcut:
    def __init__(self, data: list):
        self.name = data[0]  # string
        self.combination = data[1]  # string received using format_keys
        self.command = int(data[2])  # integer
        self.description = data[3]  # string
        raw_args = data[4]
        # When we receive data from GUI it already a list, if it is from csv file, it a json string
        if isinstance(raw_args, str):
            self.optional_arguments = json.loads(raw_args)
        else:
            self.optional_arguments = list(raw_args)

    def readable_key_sequence(self):
        return format_keys(self.combination)

    def __str__(self):
        return f"\n Name: {self.name}\n Combination: {self.combination}\n Command: {self.command}\n Description: {self.description} Optional Arguments: {self.optional_arguments}\n"

    def action(self):
        command_class = command_id_to_class[self.command]
        command_instance = command_class()
        command_instance.action(*self.optional_arguments)
