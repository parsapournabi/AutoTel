from datetime import datetime, timedelta
import sqlite3
import inspect
import os


class DataBase:
    _platform: str

    def __init__(self, platform: str):
        self._platform = platform

        path = self._create_db_file("WeaTel_session.db")

        # Creating Sql stuff
        self._sql = sqlite3.connect(path)
        self._cursor = self._sql.cursor()

        # Create Tables
        self._create_tables()

        # Deleting Expired
        self.delete_expired_tel_items()

    # Public Methods
    def insert_tel_item(self, phone: str, expiry: datetime = None):
        try:
            EXPIRY = expiry or datetime.now().replace(microsecond=0) + timedelta(days=365)
            QUERY = "INSERT INTO tel_session (phone, expiry) VALUES (?, ?);"
            self._cursor.execute(QUERY, (phone, EXPIRY))
            self._sql.commit()

        except Exception as ex:
            print(f"Exception {self.__class__.__name__}.{inspect.currentframe().f_code.co_name}\n{ex}")

    def fetch_tel_phones(self):
        try:
            QUERY = "SELECT phone FROM tel_session;"
            self._cursor.execute(QUERY)
            return self._cursor.fetchall()
        except Exception as ex:
            print(f"Exception {self.__class__.__name__}.{inspect.currentframe().f_code.co_name}\n{ex}")

    def delete_expired_tel_items(self):
        try:
            QUERY = "DELETE FROM tel_session WHERE ? >= expiry;"
            self._cursor.execute(QUERY, (datetime.now().replace(microsecond=0),))
            self._sql.commit()
        except Exception as ex:
            print(f"Exception {self.__class__.__name__}.{inspect.currentframe().f_code.co_name}\n{ex}")

    # Private Methods
    def _create_tables(self):
        """Creating info table and maybe some other tables"""
        # feedback table
        TABLE_TEL_SESSION = f'CREATE TABLE IF NOT EXISTS tel_session (phone VARCHAR(20), expiry TIMESTAMP);'
        self._cursor.execute(TABLE_TEL_SESSION)

        self._sql.commit()

    def _create_db_file(self, name: str) -> str:
        try:
            HOME_DIR = os.path.expanduser("~")
            path = os.path.join(HOME_DIR, f"Documents/{name}") if self._platform == "WINDOWS" else os.path.join(
                HOME_DIR, name)
            if not os.path.exists(path):
                file = open(path, 'w')
                file.close()
            return path
        except Exception as ex:
            print(f"Exception {self.__class__.__name__}.{inspect.currentframe().f_code.co_name}\n{ex}")
        return ""


if __name__ == '__main__':
    db = DataBase("WINDOWS")
    phones = db.fetch_tel_phones()
    print("Phones: ", phones)
    if not phones:
        print("Creating...")
        db.insert_tel_item("+98-9381123417", datetime.now().replace(microsecond=0) + timedelta(seconds=10))

        phones = db.fetch_tel_phones()
        print("Phones after: ", phones)
