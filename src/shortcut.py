from src.actions import action

class Shortcut:
    def __init__(self, data: list):
        self.name = data[0]
        self.combination = data[1]
        self.command = int(data[2])
        self.description = data[3]
        self.optional_argument = data[4]

    def action(self):
        action(self.command, self.optional_argument)
