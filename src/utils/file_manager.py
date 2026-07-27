from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal
import os


class FileManager(QObject):
    _targetPath: str = os.path.expanduser("~/Pictures/Screenshots")
    targetPathChanged = pyqtSignal()

    def __init__(self, parent=None):
        super(FileManager, self).__init__(parent=parent)

    # Public methods
    def has_new_files(self, path="") -> bool:
        _path = path or self._targetPath
        if not path:
            print("Path is empty: ", path, self._targetPath)
            return False

        files = self._get_current_files(_path)
        if not files:
            # target path has no such any files
            return False

        if self._is_files_are_new(files):
            return True
        return False

    # Properties

    @pyqtProperty(str)
    def targetPath(self) -> str:
        return self._targetPath

    @targetPath.setter
    def targetPath(self, path: str):
        if path == self._targetPath:
            return
        self._targetPath = path
        self.targetPathChanged.emit()

    # Protected & Private methods

    def _get_current_files(self, path: str) -> list:
        pass

    def _is_files_are_new(self, files: list) -> bool:
        pass
