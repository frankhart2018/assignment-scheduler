import os
import sqlite3

from .constants import DB_PATH, CREATE_TABLES_FILE_PATH


class DBInstance:
    __dbinstance = None

    @classmethod
    def __set_instance(cls):
        if cls.__dbinstance is None:
            cls.__dbinstance = sqlite3.connect(DB_PATH, check_same_thread=False)

    @classmethod
    def setup_db(cls):
        if cls.__dbinstance == None:
            cls.__set_instance()

        cursor = cls.__dbinstance.cursor()

        with open(CREATE_TABLES_FILE_PATH, "r") as file:
            cursor.executescript(file.read())

        cls.__dbinstance.commit()

    @classmethod
    def get_instance(cls):
        if not os.path.exists(DB_PATH):
            cls.setup_db()
        elif cls.__dbinstance == None:
            cls.__set_instance()

        return cls.__dbinstance
