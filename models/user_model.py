# models/user_model.py
from models.base_model import BaseModel
from typing import Optional, Dict, List, Any


class UserModel(BaseModel):
    @property
    def table_name(self):
        return "users"

    def create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        )
        """
        self._execute(query)

    def create(self, username: str, email: str, password_hash: str) -> int:
        query = f"""
        INSERT INTO {self.table_name} (username, email, password_hash)
        VALUES (?, ?, ?)
        RETURNING id
        """
        result = self._execute(query, (username, email, password_hash), fetch_all=False)
        return result["id"] if result else None

    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        query = f"SELECT * FROM {self.table_name} WHERE id = ?"
        return self._execute(query, (user_id,), fetch_all=False)

    def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        query = f"SELECT * FROM {self.table_name} WHERE username = ?"
        return self._execute(query, (username,), fetch_all=False)

    def get_all_active(self) -> List[Dict[str, Any]]:
        query = f"SELECT * FROM {self.table_name} WHERE is_active = TRUE"
        result = self._execute(query)
        return result if result else []  # Return empty list instead of None

    def update_email(self, user_id: int, new_email: str) -> bool:
        query = f"UPDATE {self.table_name} SET email = ? WHERE id = ?"
        return self._execute(query, (new_email, user_id)) > 0

    def deactivate(self, user_id: int) -> bool:
        query = f"UPDATE {self.table_name} SET is_active = FALSE WHERE id = ?"
        return self._execute(query, (user_id,)) > 0
