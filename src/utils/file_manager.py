from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal
import os


class FileManager(QObject):
    _targetPath: str = os.path.expanduser("~/Pictures/Screenshots")
    targetPathChanged = pyqtSignal()

    def __init__(self, parent=None):
        super(FileManager, self).__init__(parent=parent)

    @pyqtProperty(str)
    def targetPath(self) -> str:
        return self._targetPath

    @targetPath.setter
    def targetPath(self, path: str):
        if path == self._targetPath:
            return
        self._targetPath = path
        self.targetPathChanged.emit()
