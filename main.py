import os
import sys

from PySide6 import QtWidgets

from src.actions import stop_recording
from src.globallistener import GlobalListener
from src.mainwindow import MainWindow
from src.theme import reload_theme, set_app

os.environ.pop("QT_STYLE_OVERRIDE", None)
os.environ["QT_LOGGING_RULES"] = "qt.qpa.wayland.textinput=false"


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(False)
    set_app(app)
    reload_theme()
    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()
    global_listener = GlobalListener()
    sys.exit(app.exec())
