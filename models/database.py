import sqlite3
from typing import Optional, List, Dict, Any
from contextlib import contextmanager


class DatabaseManager:
    def __init__(self, database_path: str):
        self.database_path = database_path

    @contextmanager
    def _get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def execute(self, query: str, params: tuple = (), fetch_all: bool = True):
        """Generic method to execute queries"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)

            if cursor.description:  # if it's a SELECT query
                if fetch_all:
                    results = [dict(row) for row in cursor.fetchall()]
                    return results if results else []
                result = cursor.fetchone()
                return dict(result) if result else None
            return cursor.rowcount  # For INSERT/UPDATE/DELETE
