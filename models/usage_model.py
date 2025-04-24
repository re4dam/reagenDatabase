# models/usage_model.py
from models.base_model import BaseModel
from typing import Optional, Dict, List, Any
from datetime import date


class UsageModel(BaseModel):
    @property
    def table_name(self):
        return "Usage"

    def create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY,
            Tanggal_Terpakai DATE,
            Jumlah_Terpakai INTEGER,
            User TEXT,
            Bahan_Pendukung TEXT,
            id_identity INTEGER,
            FOREIGN KEY (id_identity) REFERENCES Identity(id)
        )
        """
        self._execute(query)

    def create(
        self,
        tanggal_terpakai: date,
        jumlah_terpakai: int,
        user: str,
        bahan_pendukung: str,
        id_identity: int,
    ) -> int:
        query = f"""
        INSERT INTO {self.table_name} (
            Tanggal_Terpakai, Jumlah_Terpakai, User, Bahan_Pendukung, id_identity
        )
        VALUES (?, ?, ?, ?, ?)
        RETURNING id
        """
        params = (tanggal_terpakai, jumlah_terpakai, user, bahan_pendukung, id_identity)
        result = self._execute(query, params, fetch_all=False)
        return result["id"] if result else None

    def get_by_id(self, usage_id: int) -> Optional[Dict[str, Any]]:
        query = f"SELECT * FROM {self.table_name} WHERE id = ?"
        return self._execute(query, (usage_id,), fetch_all=False)

    def get_all(self) -> List[Dict[str, Any]]:
        query = f"SELECT * FROM {self.table_name}"
        result = self._execute(query)
        return result if result else []

    def get_by_identity(self, identity_id: int) -> List[Dict[str, Any]]:
        query = f"SELECT * FROM {self.table_name} WHERE id_identity = ?"
        result = self._execute(query, (identity_id,))
        return result if result else []

    def get_by_user(self, user: str) -> List[Dict[str, Any]]:
        query = f"SELECT * FROM {self.table_name} WHERE User = ?"
        result = self._execute(query, (user,))
        return result if result else []

    def update(self, usage_id: int, **kwargs) -> bool:
        # Build dynamic update query based on provided fields
        set_clauses = []
        params = []

        valid_fields = [
            "Tanggal_Terpakai",
            "Jumlah_Terpakai",
            "User",
            "Bahan_Pendukung",
            "id_identity",
        ]

        for field, value in kwargs.items():
            if field in valid_fields:
                set_clauses.append(f"{field} = ?")
                params.append(value)

        if not set_clauses:
            return False  # Nothing to update

        params.append(usage_id)  # For the WHERE clause

        query = f"UPDATE {self.table_name} SET {', '.join(set_clauses)} WHERE id = ?"
        return self._execute(query, tuple(params)) > 0

    def delete(self, usage_id: int) -> bool:
        query = f"DELETE FROM {self.table_name} WHERE id = ?"
        return self._execute(query, (usage_id,)) > 0
