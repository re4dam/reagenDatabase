import sqlite3
from typing import Optional, List, Dict, Any


class DatabaseManager:
    def __init__(self, database_path: str):
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()
        self._initialize_tables()

    def _initialize_tables(self):
        """initialize database tables if they don't exist"""
        self.cursor.execute(
            """ CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) """
        )
        self.connection.commit()

    def create_record(self, name: str, description: str = ""):
        """create a new record and return its ID"""
        self.cursor.execute(
            "INSERT INTO records (name, description) VALUES (?, ?)", (name, description)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def get_records(self) -> List[Dict[str, Any]]:
        """Get all records from the database"""
        self.cursor.execute("SELECT * FROM records")
        columns = [column[0] for column in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def update_record(self, record_id: int, name: str, description: str = "") -> bool:
        # Update record by ID
        self.cursor.execute(
            "UPDATE records SET name = ?, description = ? WHERE id = ?",
            (name, description, record_id),
        )
        self.connection.commit()
        return self.cursor.rowcount > 0

    def delete_record(self, record_id: int) -> bool:
        """Delete a record by ID"""
        self.cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def __del__(self):
        """Clean up when the object is destroyed"""
        self.connection.close()
