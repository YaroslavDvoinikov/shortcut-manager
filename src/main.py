import os
import sys

from PySide6 import QtWidgets
from PySide6.QtCore import QFile, QTextStream

from src.mainwindow import MainWindow
from src.settings import Settings

os.environ.pop("QT_STYLE_OVERRIDE", None)
os.environ["QT_LOGGING_RULES"] = "qt.qpa.wayland.textinput=false"

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    settings = Settings()
    theme = settings.get_setting('theme')
    file = QFile(theme + '.qss')
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())
    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec())
