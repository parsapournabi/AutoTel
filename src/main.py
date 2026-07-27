from PyQt5.QtCore import QObject, QTimer, pyqtSlot

from src.cusqt.custom_widgets import QApplication
from src.utils.utils import ConnectionState, SessionState, ProcessState, AuthState
from src.database.sql_session import DataBase
from src.utils.file_manager import FileManager, FileInfo
from src.utils.network_manager import NetworkManager
from src.robot.telegram import Telegram

from dotenv import load_dotenv
import asyncio
import os

# Loading Project environment
load_dotenv()


class Main(QObject):
    # Private Members
    _proc_state: ProcessState = ProcessState(ProcessState.CHECK_FILES)
    _conn_state: ConnectionState = ConnectionState(ConnectionState.NO_NETWORK)
    _session_state: SessionState = SessionState(SessionState.CHECK_SESSION)
    _auth_state: AuthState = AuthState(AuthState.AUTH_PHONE)

    # API members
    db: DataBase
    file_manager: FileManager
    telegram: Telegram

    # Public Members
    user_phone: str = ""
    security_code: str = ""
    two_factor: str = ""
    available_files: list[FileInfo]

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        # Async Event Loop
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Members
        self.db = DataBase(QApplication.os_platform)
        self.file_manager = FileManager(self)

        telegram_session_path_windows: str = os.path.join(os.path.expanduser('~'), 'Documents/WeaTel_database.db')
        telegram_session_path_mac: str = os.path.join(os.path.expanduser('~'), 'WeaTel_database.db')
        self.telegram: Telegram = Telegram(api_id=os.getenv("TEL_API_ID"),
                                           api_hash=os.getenv("TEL_API_HASH"),
                                           session_name=telegram_session_path_windows if QApplication.os_platform == 'WINDOWS' else telegram_session_path_mac)

        self.available_files = []

        # Refresh Timer for Checking state
        self._timer = QTimer()
        self._timer.setInterval(1000)

        # Connections
        self._timer.timeout.connect(self._update)

    # Public Methods

    @pyqtSlot()
    def start(self):
        self._timer.start()

    # Protected & Private Methods
    def _auth_phone(self):
        print(self._auth_state)
        self._auth_state = self.loop.run_until_complete(self.telegram.connect(self.user_phone.replace("-", ""),
                                                                              self.security_code,
                                                                              self.two_factor))

    def _auth_sec_code(self):
        print(self._auth_state)
        if not self.security_code:
            self.security_code = input("Please ENTER SECURITY CODE: ")
            return
        self._auth_state = self.loop.run_until_complete(self.telegram.connect(self.user_phone.replace("-", ""),
                                                                              self.security_code,
                                                                              self.two_factor))

    def _auth_2fa(self):
        print(self._auth_state)
        if not self.two_factor:
            self.two_factor = input("Please ENTER 2FA CODE: ")
            return
        self._auth_state = self.loop.run_until_complete(self.telegram.connect(self.user_phone.replace("-", ""),
                                                                              self.security_code,
                                                                              self.two_factor))

    def _auth_success(self):
        print(self._auth_state)
        self._session_state = SessionState.CREATE_SESSION

    def _auth_failed(self):
        print(self._auth_state)

        # Restoring everything and check at first
        self._proc_state = ProcessState.CHECK_FILES
        self._conn_state = ConnectionState.NO_NETWORK
        self._session_state = SessionState.CHECK_SESSION
        self._auth_state = AuthState.AUTH_PHONE

    def _check_session(self):
        print(self._session_state)
        if phones := self.db.fetch_tel_phones():
            self.user_phone = phones[len(phones) - 1]
            # Goto next state
            self._session_state = SessionState.NO_SESSION
        else:
            self.user_phone = ""
            # Goto next state
            self._session_state = SessionState.NO_SESSION

        # Restoring Memories
        self.security_code = ""
        self.two_factor = ""
        self._auth_state = AuthState.AUTH_PHONE

    def _no_session(self):
        print(self._session_state)
        if not self.user_phone:
            self.user_phone = input("PLEASE INSERT YOUR PHONE NUMBER: ")
            return
        match self._auth_state:
            case AuthState.AUTH_PHONE:
                self._auth_phone()
            case AuthState.AUTH_SEC_CODE:
                self._auth_sec_code()
            case AuthState.AUTH_2FA:
                self._auth_2fa()
            case AuthState.AUTH_SUCCESS:
                self._auth_success()
            case AuthState.AUTH_FAILED:
                self._auth_failed()

    def _create_session(self):
        print(self._session_state)
        self.db.insert_tel_item(self.user_phone)
        self._session_state = SessionState.SESSION_EXISTS

    def _session_exists(self):
        print(self._session_state)
        self._conn_state = ConnectionState.CONNECTED

    def _no_network(self):
        print(self._conn_state)
        if NetworkManager.has_internet():
            # Goto next state
            self._conn_state = ConnectionState.NO_PROXY
        else:
            # If internet has disconnected or not connected telegram should be re-login
            self._session_state = SessionState.CHECK_SESSION

    def _no_proxy(self):
        print(self._conn_state)
        if NetworkManager.can_connect_telegram():
            # Goto next state
            self._conn_state = ConnectionState.DISCONNECTED
        else:
            # If internet has disconnected or not connected telegram should be re-login
            self._session_state = SessionState.CHECK_SESSION

    def _disconnected(self):
        print(self._conn_state)
        match self._session_state:
            case SessionState.CHECK_SESSION:
                self._check_session()
            case SessionState.NO_SESSION:
                self._no_session()
            case SessionState.CREATE_SESSION:
                self._create_session()
            case SessionState.SESSION_EXISTS:
                self._session_exists()

    def _connected(self):
        print(self._conn_state)
        self._proc_state = ProcessState.SENDING_FILES

    def _check_files(self):
        print(self._proc_state)
        if availableFiles := self.file_manager.compare_files(self.db.fetch_all_dirty_files(),
                                                             self.file_manager.get_current_files()):
            print("Available FILES: ", availableFiles, self.db.fetch_all_dirty_files())
            self.available_files = availableFiles
            # Goto next state
            self._conn_state = ConnectionState.NO_NETWORK
            self._proc_state = ProcessState.CHECK_CONNECTION

    def _check_connection(self):
        print(self._proc_state)
        match self._conn_state:
            case ConnectionState.NO_NETWORK:
                self._no_network()
            case ConnectionState.NO_PROXY:
                self._no_proxy()
            case ConnectionState.DISCONNECTED:
                self._disconnected()
            case ConnectionState.CONNECTED:
                self._connected()
            case _:
                print("DEFAULT")

    def _sending_files(self):
        print(self._proc_state)
        for file in self.available_files:
            path, hsh = file.path, file.hash
            print("Current file: ", path, hsh)
            if not os.path.exists(path):
                print("Non existing file: ", path)
                continue
            print("Uploading...", path)
            upload_res = self.loop.run_until_complete(self.telegram.upload_file_to_me(path))
            print("Upload result: ", upload_res)
            if upload_res:
                self.db.insert_dirty_file(hsh)

        self._proc_state = ProcessState.FILES_SENT

    def _files_sent(self):
        print(self._proc_state)

        # Restoring Memories (Only the safe ones)
        self._proc_state = ProcessState.CHECK_FILES

    def _update(self):
        match self._proc_state:
            case ProcessState.CHECK_FILES:
                self._check_files()
            case ProcessState.CHECK_CONNECTION:
                self._check_connection()
            case ProcessState.SENDING_FILES:
                self._sending_files()
            case ProcessState.FILES_SENT:
                self._files_sent()
            case _:
                print("Invalid State for ProcessState", self._proc_state)
