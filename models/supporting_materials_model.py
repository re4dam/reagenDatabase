# models/supporting_materials_model.py
from models.base_model import BaseModel
from typing import Optional, Dict, List, Any


class SupportingMaterialsModel(BaseModel):
    @property
    def table_name(self):
        return "SupportingMaterials"

    def create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
        """
        self._execute(query)

    def create(self, name: str) -> int:
        """
        Create a new supporting material entry or return existing one if it exists

        Args:
            name: The name of the supporting material

        Returns:
            int: The ID of the created or existing supporting material
        """
        # First check if material with this name already exists
        existing = self.get_by_name(name)
        if existing:
            return existing["id"]

        # If not, create new entry
        query = f"""
        INSERT INTO {self.table_name} (name)
        VALUES (?)
        RETURNING id
        """
        params = (name,)
        result = self._execute(query, params, fetch_all=False)
        return result["id"] if result else None

    def get_by_id(self, material_id: int) -> Optional[Dict[str, Any]]:
        query = f"SELECT * FROM {self.table_name} WHERE id = ?"
        return self._execute(query, (material_id,), fetch_all=False)

    def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        query = f"SELECT * FROM {self.table_name} WHERE LOWER(name) = LOWER(?)"
        return self._execute(query, (name,), fetch_all=False)

    def get_all(self) -> List[Dict[str, Any]]:
        query = f"SELECT * FROM {self.table_name} ORDER BY name"
        result = self._execute(query)
        return result if result else []

    def update(self, material_id: int, name: str) -> bool:
        query = f"UPDATE {self.table_name} SET name = ? WHERE id = ?"
        return self._execute(query, (name, material_id)) > 0

    def delete(self, material_id: int) -> bool:
        query = f"DELETE FROM {self.table_name} WHERE id = ?"
        return self._execute(query, (material_id,)) > 0
