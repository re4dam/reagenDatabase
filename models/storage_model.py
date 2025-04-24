# models/storage_model.py
from models.base_model import BaseModel
from typing import Optional, Dict, List, Any


class StorageModel(BaseModel):
    @property
    def table_name(self):
        return "Storage"

    def create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY,
            Name TEXT,
            Level INTEGER
        )
        """
        self._execute(query)

    def create(self, name: str, level: int) -> int:
        query = f"""
        INSERT INTO {self.table_name} (Name, Level)
        VALUES (?, ?)
        RETURNING id
        """
        result = self._execute(query, (name, level), fetch_all=False)
        return result["id"] if result else None

    def get_by_id(self, storage_id: int) -> Optional[Dict[str, Any]]:
        query = f"SELECT * FROM {self.table_name} WHERE id = ?"
        return self._execute(query, (storage_id,), fetch_all=False)

    def get_all(self) -> List[Dict[str, Any]]:
        query = f"SELECT * FROM {self.table_name}"
        result = self._execute(query)
        return result if result else []

    def update(self, storage_id: int, name: str = None, level: int = None) -> bool:
        # Build dynamic update query based on provided fields
        set_clauses = []
        params = []

        if name is not None:
            set_clauses.append("Name = ?")
            params.append(name)

        if level is not None:
            set_clauses.append("Level = ?")
            params.append(level)

        if not set_clauses:
            return False  # Nothing to update

        params.append(storage_id)  # For the WHERE clause

        query = f"UPDATE {self.table_name} SET {', '.join(set_clauses)} WHERE id = ?"
        return self._execute(query, tuple(params)) > 0

    def delete(self, storage_id: int) -> bool:
        query = f"DELETE FROM {self.table_name} WHERE id = ?"
        return self._execute(query, (storage_id,)) > 0
