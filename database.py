import sqlite3
import json
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_path='system.db'):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Connect to SQLite database"""
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        return self.connection
        
    def init_database(self):
        """Initialize database tables"""
        self.connect()
        
        # Users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # System events log
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                event_data TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Filesystem (virtual)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS filesystem (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,  -- 'file' or 'directory'
                path TEXT NOT NULL,
                content TEXT,
                size INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Settings
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                setting_key TEXT NOT NULL,
                setting_value TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create default admin user if not exists
        self.cursor.execute('''
            INSERT OR IGNORE INTO users (username, password) 
            VALUES (?, ?)
        ''', ('admin', 'password'))
        
        # Create default filesystem structure
        self.create_default_filesystem()
        
        self.connection.commit()
        
    def create_default_filesystem(self):
        """Create default filesystem structure"""
        default_structure = [
            ('/', 'directory', '', None, 0),
            ('/home', 'directory', '/', None, 0),
            ('/home/admin', 'directory', '/home', None, 0),
            ('/home/admin/Documents', 'directory', '/home/admin', None, 0),
            ('/home/admin/Downloads', 'directory', '/home/admin', None, 0),
            ('/home/admin/Pictures', 'directory', '/home/admin', None, 0),
            ('/home/admin/Music', 'directory', '/home/admin', None, 0),
            ('/etc', 'directory', '/', None, 0),
            ('/var', 'directory', '/', None, 0),
            ('/var/log', 'directory', '/var', None, 0),
            ('welcome.txt', 'file', '/home/admin', 'Welcome to Python OS Simulator!\n\nThis is a simulated operating system built with Python and Tkinter.\n\nFeatures:\n- Desktop Interface\n- Applications\n- File System\n- Settings\n- Terminal\n\nEnjoy exploring!', 1024)
        ]
        
        for name, type_, path, content, size in default_structure:
            self.cursor.execute('''
                INSERT OR IGNORE INTO filesystem (name, type, path, content, size)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, type_, path, content, size))
        
    def log_event(self, event_type, event_data=None):
        """Log system event"""
        try:
            data_str = json.dumps(event_data) if event_data else None
            self.cursor.execute('''
                INSERT INTO system_log (event_type, event_data)
                VALUES (?, ?)
            ''', (event_type, data_str))
            self.connection.commit()
        except Exception as e:
            print(f"Error logging event: {e}")
            
    def get_user_settings(self, username, key=None):
        """Get user settings"""
        self.cursor.execute('''
            SELECT s.setting_key, s.setting_value
            FROM settings s
            JOIN users u ON s.user_id = u.id
            WHERE u.username = ?
        ''', (username,))
        
        settings = dict(self.cursor.fetchall())
        return settings.get(key) if key else settings
        
    def update_user_settings(self, username, key, value):
        """Update user settings"""
        try:
            self.cursor.execute('''
                SELECT id FROM users WHERE username = ?
            ''', (username,))
            user_id = self.cursor.fetchone()[0]
            
            self.cursor.execute('''
                INSERT OR REPLACE INTO settings (user_id, setting_key, setting_value)
                VALUES (?, ?, ?)
            ''', (user_id, key, value))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating settings: {e}")
            return False
            
    def list_directory(self, path):
        """List directory contents"""
        self.cursor.execute('''
            SELECT name, type, size, modified_at
            FROM filesystem
            WHERE path = ?
            ORDER BY type, name
        ''', (path,))
        return self.cursor.fetchall()
        
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()