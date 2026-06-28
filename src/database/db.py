import sqlite3
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
import os


class Database:
    """SQLite database handler for medical records."""
    
    def __init__(self, db_path: str = "data/medical_records.db"):
        """Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection.
        
        Returns:
            SQLite connection object
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_db(self) -> None:
        """Initialize database tables."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medical_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name TEXT,
                age INTEGER,
                gender TEXT,
                symptoms TEXT,
                diagnosis TEXT,
                medicines TEXT,
                medical_history TEXT,
                doctor_name TEXT,
                hospital_name TEXT,
                summary TEXT,
                extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_record(self, record: Dict[str, Any]) -> int:
        """Save medical record to database.
        
        Args:
            record: Medical record dictionary
            
        Returns:
            ID of inserted record
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO medical_records (
                patient_name, age, gender, symptoms, diagnosis,
                medicines, medical_history, doctor_name, hospital_name, summary, extracted_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record.get("patient_name"),
            record.get("age"),
            record.get("gender"),
            json.dumps(record.get("symptoms", [])),
            record.get("diagnosis"),
            json.dumps(record.get("medications", [])),
            json.dumps(record.get("medical_history", [])),
            record.get("doctor_name"),
            record.get("hospital_name"),
            record.get("summary"),
            record.get("extracted_at", datetime.now().isoformat())
        ))
        
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return record_id
    
    def get_record(self, record_id: int) -> Optional[Dict[str, Any]]:
        """Get medical record by ID.
        
        Args:
            record_id: Record ID
            
        Returns:
            Medical record dictionary or None
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM medical_records WHERE id = ?", (record_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_dict(row)
        return None
    
    def get_all_records(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all medical records with pagination.
        
        Args:
            limit: Maximum number of records to return
            offset: Offset for pagination
            
        Returns:
            List of medical record dictionaries
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM medical_records 
            ORDER BY extracted_at DESC 
            LIMIT ? OFFSET ?
        """, (limit, offset))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def search_records(self, query: str) -> List[Dict[str, Any]]:
        """Search medical records by patient name or diagnosis.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching medical records
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        search_pattern = f"%{query}%"
        cursor.execute("""
            SELECT * FROM medical_records 
            WHERE patient_name LIKE ? OR diagnosis LIKE ?
            ORDER BY extracted_at DESC
        """, (search_pattern, search_pattern))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def delete_record(self, record_id: int) -> bool:
        """Delete medical record by ID.
        
        Args:
            record_id: Record ID
            
        Returns:
            True if deleted, False if not found
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM medical_records WHERE id = ?", (record_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
    
    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """Convert database row to dictionary.
        
        Args:
            row: SQLite row object
            
        Returns:
            Dictionary representation of the row
        """
        return {
            "id": row["id"],
            "patient_name": row["patient_name"],
            "age": row["age"],
            "gender": row["gender"],
            "symptoms": json.loads(row["symptoms"]) if row["symptoms"] else [],
            "diagnosis": row["diagnosis"],
            "medications": json.loads(row["medicines"]) if row["medicines"] else [],
            "medical_history": json.loads(row["medical_history"]) if row["medical_history"] else [],
            "doctor_name": row["doctor_name"],
            "hospital_name": row["hospital_name"],
            "summary": row["summary"],
            "extracted_at": row["extracted_at"]
        }