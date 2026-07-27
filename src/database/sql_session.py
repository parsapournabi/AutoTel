from datetime import datetime, timedelta
import sqlite3
import inspect
import os


class DataBase:
    _platform: str

    def __init__(self, platform: str):
        self._platform = platform

        path = self._create_db_file("WeaTel.db")

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

    def insert_dirty_file(self, file: str):
        try:
            QUERY = "INSERT OR IGNORE INTO dirty_files VALUES (?);"
            self._cursor.execute(QUERY, (file,))
            self._sql.commit()
        except Exception as ex:
            print(f"Exception {self.__class__.__name__}.{inspect.currentframe().f_code.co_name}\n{ex}")

    def insert_dirty_files(self, files: list[str]):
        try:
            QUERY = "INSERT OR IGNORE INTO dirty_files VALUES (?);"
            self._cursor.executemany(QUERY, ((file_hash,) for file_hash in files))
            self._sql.commit()
        except Exception as ex:
            print(f"Exception {self.__class__.__name__}.{inspect.currentframe().f_code.co_name}\n{ex}")

    def fetch_tel_phones(self):
        try:
            QUERY = "SELECT phone FROM tel_session;"
            self._cursor.execute(QUERY)
            return list(map(lambda x: x[0], self._cursor.fetchall()))
        except Exception as ex:
            print(f"Exception {self.__class__.__name__}.{inspect.currentframe().f_code.co_name}\n{ex}")

    def fetch_all_dirty_files(self) -> list[str]:
        try:
            QUERY = "SELECT * FROM dirty_files;"
            self._cursor.execute(QUERY)
            return list(map(lambda x: x[0], self._cursor.fetchall()))
        except Exception as ex:
            print(f"Exception {self.__class__.__name__}.{inspect.currentframe().f_code.co_name}\n{ex}")
        return []

    def delete_expired_tel_items(self):
        try:
            QUERY = "DELETE FROM tel_session WHERE ? >= expiry;"
            self._cursor.execute(QUERY, (datetime.now().replace(microsecond=0),))
            self._sql.commit()
        except Exception as ex:
            print(f"Exception {self.__class__.__name__}.{inspect.currentframe().f_code.co_name}\n{ex}")

    def delete_all_dirty_files(self):
        try:
            QUERY = "DELETE FROM dirty_files;"
            self._cursor.execute(QUERY)
            self._sql.commit()
        except Exception as ex:
            print(f"Exception {self.__class__.__name__}.{inspect.currentframe().f_code.co_name}\n{ex}")

    # Private Methods
    def _create_tables(self):
        """Creating info table and maybe some other tables"""
        # feedback table
        TABLE_TEL_SESSION = f'CREATE TABLE IF NOT EXISTS tel_session (phone VARCHAR(20), expiry TIMESTAMP);'
        self._cursor.execute(TABLE_TEL_SESSION)

        # Files Table
        TABLE_DIRTY_FILES = "CREATE TABLE IF NOT EXISTS dirty_files (hash VARCHAR(64));"
        self._cursor.execute(TABLE_DIRTY_FILES)

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
    print(db.fetch_all_dirty_files())
    db.insert_dirty_file("Salam")
    print(db.fetch_all_dirty_files())
    lst = ["SALAM", "HOASHD", "BAND", "Parsa"]
    db.insert_dirty_files(lst)
    print(db.fetch_all_dirty_files())
    f = db.fetch_all_dirty_files()
    print(f, type(f), type(f[0]))
    db.delete_all_dirty_files()
    print(db.fetch_all_dirty_files())
    # phones = db.fetch_tel_phones()
    # print("Phones: ", phones)
    # if not phones:
    #     print("Creating...")
    #     db.insert_tel_item("+98-9381123417", datetime.now().replace(microsecond=0) + timedelta(seconds=10))
    #
    #     phones = db.fetch_tel_phones()
    #     print("Phones after: ", phones)
