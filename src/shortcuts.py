import csv
import os

from src.shortcut import Shortcut


class Shortcuts:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Shortcuts, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__shortcuts = {}
        if not os.path.isfile("shortcuts.csv"):
            open("shortcuts.csv", "w").close()
        else:
            with open("shortcuts.csv", "r") as file:
                reader = csv.reader(file)
                for line in reader:
                    shortcut = Shortcut(line)
                    self.__shortcuts[shortcut.combination] = shortcut

    def replace_shortcuts_file(self, path: str):
        self.__shortcuts.clear()
        with open(path, "r") as file:
            reader = csv.reader(file)
            for line in reader:
                shortcut = Shortcut(line)
                self.__shortcuts[shortcut.combination] = shortcut

    def save_shortcuts_file(self, path: str):
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_NONE)
            for shortcut in self.__shortcuts.values():
                writer.writerow(
                    [
                        shortcut.name,
                        shortcut.combination,
                        shortcut.command,
                        shortcut.description,
                        shortcut.optional_argument,
                    ]
                )

    def get_shortcuts(self) -> dict:
        return self.__shortcuts

    def add(self, shortcut: Shortcut):
        self.__shortcuts[shortcut.combination] = shortcut

    def remove(self, combination):
        del self.__shortcuts[combination]

    def update(self, combination, shortcut: Shortcut):
        self.__shortcuts[combination] = shortcut
