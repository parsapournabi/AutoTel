from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal
from dataclasses import dataclass
import hashlib
import os
import inspect

from src.utils.global_logic import iter_files


@dataclass(slots=True, frozen=True)
class FileInfo:
    path: str
    hash: str


class FileManager(QObject):
    _targetPath: str = os.path.join(os.path.expanduser("~"), "Pictures/Screenshots")
    targetPathChanged = pyqtSignal()

    def __init__(self, parent=None):
        super(FileManager, self).__init__(parent=parent)

    # Public methods
    @staticmethod
    def file_hash(path: str) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(1024 * 1024):
                h.update(chunk)
        return h.hexdigest()

    def get_current_files(self, path: str = "") -> list[FileInfo]:
        try:
            path = path or self._targetPath
            if not os.path.exists(path):
                print("Target path isn't exists!", path)
                return []
            if not os.path.isdir(path):
                print("Target path isn't directory", path)
                return []
            return [FileInfo(path=file, hash=self.file_hash(file)) for file in iter_files(path)]

        except Exception as ex:
            print(f"Exception {self.__class__.__name__}.{inspect.currentframe().f_code.co_name}\n{ex}")
        return []

    @staticmethod
    def compare_files(oldFiles: list[str], newFiles: list[FileInfo]) -> list[FileInfo]:
        """
        Comparing oldFiles hash with newFiles hash then return the non-existing files by FileInfo
        :param oldFiles: a list of the oldFiles hash
        :param newFiles: a list of current existing files by FileInfo
        :return: non-existing files by FileInfo
        """
        oldHash = set(oldFiles)
        return list(filter(lambda file: file.hash not in oldHash, newFiles))

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


if __name__ == '__main__':
    fmng = FileManager()
    print(FileManager.compare_files(["Parsa"], [FileInfo("", "Parsa")]))
