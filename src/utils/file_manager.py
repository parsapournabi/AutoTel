from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal
from global_logic import iter_files
import os
import inspect


class FileManager(QObject):
    _targetPath: str = os.path.join(os.path.expanduser("~"), "Pictures/Screenshots")
    targetPathChanged = pyqtSignal()

    def __init__(self, parent=None):
        super(FileManager, self).__init__(parent=parent)

    # Public methods
    def has_new_files(self, path="") -> bool:
        _path = path or self._targetPath
        if not _path:
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
        try:
            if not os.path.exists(path):
                print("Target path isn't exists!", path)
                return []
            if not os.path.isdir(path):
                print("Target path isn't directory", path)
                return []
            return list(iter_files(path))

        except Exception as ex:
            print(f"Exception {self.__class__.__name__}.{inspect.currentframe().f_code.co_name}\n{ex}")
        return []

    def _is_files_are_new(self, files: list) -> bool:
        pass


if __name__ == '__main__':
    fmng = FileManager()
    fmng.has_new_files()
