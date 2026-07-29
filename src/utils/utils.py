from enum import IntEnum, auto


class FileState(IntEnum):
    """
    Before everything the specific path should be check for new files to upload

    NO_SUCH_FILES: after an interval the  path should be recheck until the new files available
    HAS_NEW_FILES: if any new file exists, the ConnectionState & SessionState should be in next role until the new files going to upload
    """
    NO_SUCH_FILES = auto()
    HAS_NEW_FILES = auto()


class ConnectionState(IntEnum):
    """
    Telegram ConnectionState flags

    NO_NETWORK: if no WLAN or LAN is connected
    NO_PROXY: if Network is available but system proxy or tun mode is disabled
    DISCONNECTED: if Network & Proxy is available but Telegram Login is required (First check DataBase Session)
    CONNECTED: if everything is Ok and connected
    """
    NO_NETWORK = auto()
    NO_PROXY = auto()
    DISCONNECTED = auto()
    CONNECTED = auto()


class AuthState(IntEnum):
    """
    Telegram Authorization State
    AUTH_PHONE: apply login using phone number
    AUTH_SEC_CODE: apply security code
    AUTH_2FA: optional apply 2fa
    AUTH_SUCCESS: Everything fine and auth completed (next state is saving phone number session)
    AUTH_FAILED: process failed and should be start at first state
    """
    AUTH_PHONE = auto()
    AUTH_SEC_CODE = auto()
    AUTH_2FA = auto()
    AUTH_SUCCESS = auto()
    AUTH_FAILED = auto()


class SessionState(IntEnum):
    """
    Database Session state using self DataBase (sqlite)

    CHECK_SESSION: fetching session from TABLE .
    NO_SESSION: after fetch if it is empty.
    CREATE_SESSION: if no session it should be recreate.
    SESSION_EXISTS: while checking if session exists
    """
    CHECK_SESSION = auto()
    NO_SESSION = auto()
    CREATE_SESSION = auto()
    SESSION_EXISTS = auto()


class ProcessState(IntEnum):
    """
    Overall State process
    CHECK_FILES: referrer FileState
    CHECK_CONNECTION: referrer ConnectionState, SessionState
    SENDING_FILES: sending each file to the telegram direct
        NOTE: before sending via telegram check if file exists
        (in this process for each file after sent it should be store in DataBase)
    FILES_SENT: last state it should be reset all of memories and re-processing by CHECK_FILES
    """
    CHECK_FILES = auto()
    CHECK_CONNECTION = auto()
    SENDING_FILES = auto()
    FILES_SENT = auto()


class NotificationType(IntEnum):
    """
    QSystemTrayIcon notification
    INFO: information type
    WARNING: warning type
    ERROR: Critical type
    """
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
