from PyQt5.QtCore import QObject, QTimer, pyqtSlot


class Main(QObject):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        # Refresh Timer for Checking state
        self._timer = QTimer()
        self._timer.setInterval(1000)

        # Connections
        self._timer.timeout.connect(self._updateFrame)

        print("Main has created: ", self)

    # Public Methods

    @pyqtSlot()
    def start(self):
        print("Starting timer...")
        self._timer.start()

    # Protected & Private Methods
    def _updateFrame(self):
        print("onTimer Triggered")
