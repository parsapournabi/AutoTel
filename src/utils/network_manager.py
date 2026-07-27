import socket
import inspect


class NetworkManager:
    """
    NetworkManager handles network & Internet status
    also provides proxy checking state
    """

    def __init__(self):
        pass

    @staticmethod
    def has_internet(host="8.8.8.8", port=53, timeout=3) -> bool:
        """
        :param host: Target host for TCP/ICMP connection
        :param port: Target server port
        :param timeout: unit by seconds
        :return: bool -> if has Internet == True
        """
        try:
            socket.setdefaulttimeout(timeout)
            socket.create_connection((host, port))
            return True
        except OSError:
            pass
        except Exception as ex:
            print(f"Exception {NetworkManager.__class__.__name__}.{inspect.currentframe().f_code.co_name}\n{ex}")
        return False

    @staticmethod
    def can_connect_telegram(timeout=3) -> bool:
        """
        :param timeout: unit per second
        :return: bool --> if can connect to the telegram == True
        """
        try:
            TELEGRAM_SERVER_HOST: str = "149.154.167.51"
            TELEGRAM_SERVER_PORT: int = 443
            socket.create_connection((TELEGRAM_SERVER_HOST, TELEGRAM_SERVER_PORT), timeout)
            return True
        except OSError:
            pass
        except Exception as ex:
            print(f"Exception {NetworkManager.__class__.__name__}.{inspect.currentframe().f_code.co_name}\n{ex}")
        return False
