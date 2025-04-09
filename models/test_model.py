# models/test_model.py
from models.base_model import BaseModel
from typing import Optional, Dict, List, Any


class TestModel(BaseModel):
    @property
    def table_name(self):
        return "records"

    def create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXIST {self.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self._execute(query)
