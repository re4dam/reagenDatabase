# models/test_model.py
from models.base_model import BaseModel
from typing import Optional, Dict, List, Any

class RecordModel(BaseModel):
    @property
    def table_name(self):
        return "records"

    def create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self._execute(query)

    def create_record(self, name: str, description: str) -> int:
        query = f"""
        INSERT INTO {self.table_name} (name, description)
        VALUES (?, ?)
        RETURNING id
        """
        result = self._execute(query, (name, description), fetch_all=False)
        return result["id"] if result else None

    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        query = f"SELECT * FROM {self.table_name} WHERE id = ?"
        return self._execute(query, (user_id,), fetch_all=False)

    def get_all(self) -> List[Dict[str, Any]]:
        query = f"SELECT * FROM {self.table_name}"
        result = self._execute(query)
        return result if result else []  # Return empty list instead of None

    def update_record(self, user_id: int, new_name: str, new_description: str) -> bool:
        query = (
            f"UPDATE {self.table_name} SET name = ?, SET description = ? WHERE id = ?"
        )
        return self._execute(query, (new_name, new_description, user_id)) > 0

    def delete_record(self, user_id: int) -> bool:
        query = f"DELETE FROM {self.table_name} WHERE id = ?"
        return self._execute(query, (user_id,)) > 0
