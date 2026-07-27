from enum import IntEnum, auto


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


class SessionState(IntEnum):
    """
    Telegram Session state using self DataBase (sqlite)

    CHECK_SESSION: fetching session from TABLE .
    NO_SESSION: after fetch if it is empty.
    CREATE_SESSION: if no session it should be recreate.
    SESSION_EXISTS: while checking if session exists
    """
    CHECK_SESSION = auto()
    NO_SESSION = auto()
    CREATE_SESSION = auto()
    SESSION_EXISTS = auto()
