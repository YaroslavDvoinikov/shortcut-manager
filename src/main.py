import os
import sys

from PySide6 import QtWidgets

from src.mainwindow import MainWindow

os.environ.pop("QT_STYLE_OVERRIDE", None)
os.environ["QT_LOGGING_RULES"] = "qt.qpa.wayland.textinput=false"

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec())
