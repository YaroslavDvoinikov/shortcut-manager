import json

from src.actions import action


class Shortcut:
    def __init__(self, data: list):
        self.name = data[0]
        self.combination = data[1]
        self.command = int(data[2])
        self.description = data[3]
        self.optional_arguments = []
        raw_args = data[4]

        # When we receive data from GUI it already a list, if it is from csv file, it a json string
        if isinstance(raw_args, str):
            self.optional_arguments = json.loads(raw_args)
        else:
            self.optional_arguments = list(raw_args)

    def action(self):
        action(self.command, *self.optional_arguments)

    def __str__(self):
        return f"{self.name}, {self.combination}, {self.command}, {self.description}, {self.optional_arguments}"
