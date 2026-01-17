"""
Database models for job tracking
"""
import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional


class Database:
    """Simple SQLite database manager"""
    
    def __init__(self, db_path: str = "jobs.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Jobs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT,
                description TEXT NOT NULL,
                url TEXT,
                status TEXT DEFAULT 'saved',
                match_score REAL DEFAULT 0.0,
                keyword_gaps TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Resume table (stores the current resume)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resume (
                id INTEGER PRIMARY KEY,
                content TEXT NOT NULL,
                filename TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def add_job(self, title: str, company: str, description: str, 
                url: str = "", status: str = "saved") -> int:
        """Add a new job"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO jobs (title, company, description, url, status)
            VALUES (?, ?, ?, ?, ?)
        """, (title, company, description, url, status))
        
        job_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return job_id
    
    def get_all_jobs(self) -> List[Dict]:
        """Get all jobs"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM jobs ORDER BY match_score DESC, created_at DESC
        """)
        
        jobs = [dict(row) for row in cursor.fetchall()]
        
        # Parse keyword_gaps JSON
        for job in jobs:
            if job['keyword_gaps']:
                job['keyword_gaps'] = json.loads(job['keyword_gaps'])
            else:
                job['keyword_gaps'] = []
        
        conn.close()
        return jobs
    
    def get_job(self, job_id: int) -> Optional[Dict]:
        """Get a specific job"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        row = cursor.fetchone()
        
        if row:
            job = dict(row)
            if job['keyword_gaps']:
                job['keyword_gaps'] = json.loads(job['keyword_gaps'])
            else:
                job['keyword_gaps'] = []
            conn.close()
            return job
        
        conn.close()
        return None
    
    def update_job(self, job_id: int, **kwargs):
        """Update a job"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build update query dynamically
        fields = []
        values = []
        
        for key, value in kwargs.items():
            if key in ['title', 'company', 'description', 'url', 'status', 'match_score']:
                fields.append(f"{key} = ?")
                values.append(value)
            elif key == 'keyword_gaps':
                fields.append("keyword_gaps = ?")
                values.append(json.dumps(value))
        
        if fields:
            fields.append("updated_at = CURRENT_TIMESTAMP")
            values.append(job_id)
            
            query = f"UPDATE jobs SET {', '.join(fields)} WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()
        
        conn.close()
    
    def delete_job(self, job_id: int):
        """Delete a job"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        conn.commit()
        conn.close()
    
    def save_resume(self, content: str, filename: str):
        """Save or update resume"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Delete old resume (we only keep one)
        cursor.execute("DELETE FROM resume")
        
        # Insert new resume
        cursor.execute("""
            INSERT INTO resume (id, content, filename)
            VALUES (1, ?, ?)
        """, (content, filename))
        
        conn.commit()
        conn.close()
    
    def get_resume(self) -> Optional[Dict]:
        """Get the current resume"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM resume WHERE id = 1")
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return dict(row)
        return None

