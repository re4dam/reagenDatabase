from typing import List, Dict, Any, Optional


class BaseModel:
    def __init__(self, db):
        self.db = db
        self.create_table()

    @property
    def table_name(self) -> str:
        raise NotImplementedError("SubClasses must implement table_name")

    def create_table(self):
        raise NotImplementedError("SubClasses must implement create_table")

    def _execute(self, query: str, params: tuple = (), fetch_all: bool = True):
        return self.db.execute(query, params, fetch_all)
