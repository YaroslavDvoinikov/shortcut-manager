import csv
import json
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
            with open("shortcuts.csv", "w") as file:
                pass
        else:
            with open("shortcuts.csv", "r") as file:
                reader = csv.reader(file)
                for line in reader:
                    line[4] = json.loads(line[4])
                    shortcut = Shortcut(line)
                    self.__shortcuts[shortcut.combination] = shortcut

    def replace_shortcuts_file(self, path: str):
        self.__shortcuts.clear()
        with open(path, "r") as file:
            reader = csv.reader(file)
            for line in reader:
                line[4] = json.loads(line[4])
                shortcut = Shortcut(line)
                self.__shortcuts[shortcut.combination] = shortcut
        self.update_shortcuts_file()

    def save_shortcuts_file(self, path: str):
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for shortcut in self.__shortcuts.values():
                writer.writerow(
                    [
                        shortcut.name,
                        shortcut.combination,
                        shortcut.command,
                        shortcut.description,
                        json.dumps(shortcut.optional_arguments, ensure_ascii=False),
                    ]
                )

    def get_shortcuts(
        self,
    ) -> dict:
        return self.__shortcuts

    def update_shortcuts_file(self, shortcut_to_add=None, shortcut_to_remove=None):
        if shortcut_to_add:
            self.__shortcuts[shortcut_to_add.combination] = shortcut_to_add
        if shortcut_to_remove:
            del self.__shortcuts[shortcut_to_remove.combination]
        with open("shortcuts.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for shortcut in self.__shortcuts.values():
                writer.writerow(
                    [
                        shortcut.name,
                        shortcut.combination,
                        shortcut.command,
                        shortcut.description,
                        json.dumps(shortcut.optional_arguments, ensure_ascii=False),
                    ]
                )

    # def replace_settings_file(self, path: str):
    #     with open(path, "r") as file:
    #         self.__settings = json.load(file)
    #     with open("settings.json", "w") as file:
    #         txt = json.dumps(self.__settings)
    #         file.write(txt)

    # def save_settings_file(self, path: str):
    #     with open(path, "w") as file:
    #         txt = json.dumps(self.__settings)
    #         file.write(txt)
