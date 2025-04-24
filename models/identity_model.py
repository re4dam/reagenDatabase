# models/identity_model.py
from models.base_model import BaseModel
from typing import Optional, Dict, List, Any
from datetime import date


class IdentityModel(BaseModel):
    @property
    def table_name(self):
        return "Identity"

    def create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY,
            Name TEXT,
            Description TEXT,
            Wujud TEXT,
            Stock INTEGER,
            Massa INTEGER,
            Tanggal_Expire DATE,
            Category_Hazard TEXT,
            Sifat TEXT,
            Tanggal_Produksi DATE,
            Tanggal_Pembelian DATE,
            SDS TEXT,
            id_storage INTEGER,
            FOREIGN KEY (id_storage) REFERENCES Storage(id)
        )
        """
        self._execute(query)

    def create(
        self,
        name: str,
        description: str,
        wujud: str,
        stock: int,
        massa: int,
        tanggal_expire: date,
        category_hazard: str,
        sifat: str,
        tanggal_produksi: date,
        tanggal_pembelian: date,
        sds: str,
        id_storage: int,
    ) -> int:
        query = f"""
        INSERT INTO {self.table_name} (
            Name, Description, Wujud, Stock, Massa, Tanggal_Expire,
            Category_Hazard, Sifat, Tanggal_Produksi, Tanggal_Pembelian,
            SDS, id_storage
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        RETURNING id
        """
        params = (
            name,
            description,
            wujud,
            stock,
            massa,
            tanggal_expire,
            category_hazard,
            sifat,
            tanggal_produksi,
            tanggal_pembelian,
            sds,
            id_storage,
        )
        result = self._execute(query, params, fetch_all=False)
        return result["id"] if result else None

    def get_by_id(self, identity_id: int) -> Optional[Dict[str, Any]]:
        query = f"SELECT * FROM {self.table_name} WHERE id = ?"
        return self._execute(query, (identity_id,), fetch_all=False)

    def get_all(self) -> List[Dict[str, Any]]:
        query = f"SELECT * FROM {self.table_name}"
        result = self._execute(query)
        return result if result else []

    def get_by_storage(self, storage_id: int) -> List[Dict[str, Any]]:
        query = f"SELECT * FROM {self.table_name} WHERE id_storage = ?"
        result = self._execute(query, (storage_id,))
        return result if result else []

    def update(self, identity_id: int, **kwargs) -> bool:
        # Build dynamic update query based on provided fields
        set_clauses = []
        params = []

        valid_fields = [
            "Name",
            "Description",
            "Wujud",
            "Stock",
            "Massa",
            "Tanggal_Expire",
            "Category_Hazard",
            "Sifat",
            "Tanggal_Produksi",
            "Tanggal_Pembelian",
            "SDS",
            "id_storage",
        ]

        for field, value in kwargs.items():
            if field in valid_fields:
                set_clauses.append(f"{field} = ?")
                params.append(value)

        if not set_clauses:
            return False  # Nothing to update

        params.append(identity_id)  # For the WHERE clause

        query = f"UPDATE {self.table_name} SET {', '.join(set_clauses)} WHERE id = ?"
        return self._execute(query, tuple(params)) > 0

    def delete(self, identity_id: int) -> bool:
        query = f"DELETE FROM {self.table_name} WHERE id = ?"
        return self._execute(query, (identity_id,)) > 0
