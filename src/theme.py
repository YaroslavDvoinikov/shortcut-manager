from PySide6.QtCore import QFile, QTextStream

from src.settings import Settings

app = None


def set_app(qapp):
    global app
    app = qapp


def reload_theme():
    if app is None:
        print("QApplication not set for theme")
        return
    settings = Settings()
    theme = settings.get_setting("theme")
    file = QFile(theme + ".qss")
    if not file.open(QFile.ReadOnly | QFile.Text):
        print(f"Could not open theme file: {theme}.qss")
        return
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())
