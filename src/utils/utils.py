from enum import IntEnum, auto


class ConnectionState(IntEnum):
    """
    Telegram ConnectionState flags

    NO_NETWORK: if no WLAN or LAN is connected
    NO_PROXY: if Network is available but system proxy or tun mode is disabled
    DISCONNECTED: if Network & Proxy is available but Telegram Login is required
    CONNECTED: if everything is Ok and connected
    """
    NO_NETWORK = auto()
    NO_PROXY = auto()
    DISCONNECTED = auto()
    CONNECTED = auto()
