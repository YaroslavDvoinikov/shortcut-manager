import json
import os.path

class Settings:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Settings, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if not os.path.isfile('settings.json'):
            with open('settings.json', 'w') as file:
                self.__settings = {'theme': 'light'}
                txt = json.dumps(self.__settings)
                file.write(txt)
        else:
            with open('settings.json', 'r') as file:
                self.__settings = json.load(file)

    def get_setting(self, name: str) -> str:
        return self.__settings[name]

    def set_setting(self, name: str, value: str) -> None:
        self.__settings[name] = value
        with open('settings.json', 'w') as file:
            txt = json.dumps(self.__settings)
            file.write(txt)

    def replace_settings_file(self, path: str):
        with open(path, 'r') as file:
            self.__settings = json.load(file)
        with open('settings.json', 'w') as file:
            txt = json.dumps(self.__settings)
            file.write(txt)

    def save_settings_file(self, path: str):
        with open(path, 'w') as file:
            txt = json.dumps(self.__settings)
            file.write(txt)
