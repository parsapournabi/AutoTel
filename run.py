# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQuickControls2 import QQuickStyle

from untitled14.qml.Engine import Engine


if __name__ == "__main__":
    QQuickStyle.setStyle("Fusion")
    app = QGuiApplication(sys.argv)
    engine = Engine()
    engine.addImportPath(Path(__file__).parent)
    engine.loadFromModule("untitled14", "Main")
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
