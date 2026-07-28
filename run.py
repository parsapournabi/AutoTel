# This Python file uses the following encoding: utf-8
from src.cusqt.custom_widgets import QApplication
from src.main import Main

from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QSystemTrayIcon
from PyQt5.QtGui import QFontDatabase
import traceback
import sys
import os
from src.meta import resources_rc


def exception_handler(exc_type, exc_value, exc_traceback):
    """
    Custom exception handler to avoid application crash.
    Explanation -> When Unexpected error raised and it is not on try: except:
    sequence, This method will call and the traceback_email_flatlay send the errors to supports.
    """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    error_message = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f"Application has been crashed! : {error_message}\n")


os.environ["QT_FONT_DPI"] = "96"

platform: str = 'WINDOWS'
version: str = '1.0.0'

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Configuring system font
    if getattr(sys, 'frozen', False):
        # Only at pyinstaller building
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    # bold_id = QFontDatabase.addApplicationFont(os.path.join(base_path, "src/gui/fonts/AvenirNextLTPro-Bold.otf"))
    # It_id = QFontDatabase.addApplicationFont(os.path.join(base_path, "src/gui/fonts/AvenirNextLTPro-It.otf"))
    # reg_id = QFontDatabase.addApplicationFont(os.path.join(base_path, "src/gui/fonts/AvenirNextLTPro-Regular.otf"))
    # if bold_id > 0:
    #     QApplication.bold_font_family = QFontDatabase.applicationFontFamilies(bold_id)[0]
    # if It_id > 0:
    #     QApplication.italic_font_family = QFontDatabase.applicationFontFamilies(It_id)[0]
    # if reg_id > 0:
    #     QApplication.regular_font_family = QFontDatabase.applicationFontFamilies(reg_id)[0]
    # Fonts configured

    sys.excepthook = exception_handler
    app.os_platform = platform
    if app.check_if_another_instance():
        if not QSystemTrayIcon.isSystemTrayAvailable():
            sys.exit(1)
        app.setQuitOnLastWindowClosed(False)

    engine = QQmlApplicationEngine()

    # Context Properties
    _main = Main()
    engine.rootContext().setContextProperty("_main", _main)

    engine.addImportPath(os.curdir.join("qml/"))
    engine.addImportPath("qml/")
    engine.load("qml/main.qml")
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
