# This Python file uses the following encoding: utf-8
import sys
from src.meta import resources_rc

from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine


if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load("qrc:/qml/main.qml")
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
