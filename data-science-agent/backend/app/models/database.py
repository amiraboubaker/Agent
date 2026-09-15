import sqlite3
from pathlib import Path
from threading import Lock

from app.core.config import get_settings


class Database:
    def __init__(self) -> None:
        self._lock = Lock()
        self._connection: sqlite3.Connection | None = None

    def connect(self) -> sqlite3.Connection:
        if self._connection is None:
            database_url = get_settings().database_url
            database_path = database_url.removeprefix("sqlite:///")
            Path(database_path).parent.mkdir(parents=True, exist_ok=True)
            self._connection = sqlite3.connect(database_path, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
            self._connection.execute(
                """CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    task_type TEXT NOT NULL,
                    messages TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )"""
            )
            self._connection.commit()
        return self._connection

    def execute(self, query: str, parameters: tuple = ()) -> sqlite3.Cursor:
        with self._lock:
            cursor = self.connect().execute(query, parameters)
            self.connect().commit()
            return cursor


database = Database()
