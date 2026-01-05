from threading import Thread

from pynput import keyboard

from src.keynormalize import format_keys
from src.shortcuts import Shortcuts

shortcut_list = Shortcuts().get_shortcuts()


class GlobalListener:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(GlobalListener, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.current_keys = set()
        self.triggered = False

        self.listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )
        self.listener_thread = Thread(target=self.listener.run, daemon=True)
        self.listener_thread.start()

    def on_press(self, key):
        self.current_keys.add(key)
        if self.triggered:
            return
        formatted_input = format_keys(self.current_keys)
        if formatted_input in shortcut_list:
            self.triggered = True
            shortcut_list[formatted_input].action()
        if not formatted_input:
            return

    def on_release(self, key):
        if key in self.current_keys:
            self.current_keys.discard(key)

        self.triggered = False

    def reload_shortcuts(cls):
        global shortcut_list
        shortcut_list = Shortcuts().get_shortcuts()
