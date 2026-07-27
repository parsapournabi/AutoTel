from PyQt5.QtCore import QObject, QTimer, pyqtSlot

from src.utils.utils import ConnectionState
from src.utils.network_manager import NetworkManager


class Main(QObject):
    _conn_state: ConnectionState = ConnectionState(ConnectionState.NO_NETWORK)

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        # Refresh Timer for Checking state
        self._timer = QTimer()
        self._timer.setInterval(1000)

        # Connections
        self._timer.timeout.connect(self._updateFrame)

    # Public Methods

    @pyqtSlot()
    def start(self):
        self._timer.start()

    # Protected & Private Methods
    def _updateFrame(self):
        match self._conn_state:
            case ConnectionState.NO_NETWORK:
                print("NO_NETWORK")
            case ConnectionState.NO_PROXY:
                print("NO_PROXY")
            case ConnectionState.DISCONNECTED:
                print("DISCONNECTED")
            case ConnectionState.CONNECTED:
                print("CONNECTED")
            case _:
                print("DEFAULT")

