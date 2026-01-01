# database.py - Enhanced with user management
import sqlite3
import json
from datetime import datetime
import os
import hashlib

class DatabaseManager:
    def __init__(self, db_path='system.db'):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Connect to SQLite database"""
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.connection.row_factory = sqlite3.Row  # Return rows as dictionaries
        return self.connection
        
    def init_database(self):
        """Initialize database tables with first boot support"""
        self.connect()
        
        # System info table (for first boot detection)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_info (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        # Check if setup completed
        self.cursor.execute("SELECT value FROM system_info WHERE key='setup_completed'")
        result = self.cursor.fetchone()
        
        if not result:
            # First boot - setup not completed yet
            print("First boot detected - setup required")
        
        # Users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT,
                email TEXT,
                is_admin BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                profile_pic TEXT
            )
        ''')
        
        # System events log
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                event_data TEXT,
                severity TEXT DEFAULT 'info',
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Filesystem (virtual)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS filesystem (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                path TEXT NOT NULL,
                content TEXT,
                size INTEGER DEFAULT 0,
                permissions TEXT DEFAULT 'rw-r--r--',
                owner TEXT DEFAULT 'admin',
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
        
        # Installed applications
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS installed_apps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                version TEXT,
                author TEXT,
                description TEXT,
                entry_point TEXT,
                icon_path TEXT,
                category TEXT,
                is_system_app BOOLEAN DEFAULT 0,
                installed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User sessions
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_token TEXT,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP,
                ip_address TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create default users
        self.create_default_users()
        
        # Create default filesystem structure
        self.create_default_filesystem()
        
        # Create default settings
        self.create_default_settings()
        
        self.connection.commit()
        
    def hash_password(self, password):
        """Hash password for storage"""
        return hashlib.sha256(password.encode()).hexdigest()
        
    def create_default_users(self):
        """Create default users"""
        default_users = [
            ('admin', 'password', 'Administrator', 'admin@system.local', 1),
            ('user', 'password', 'Standard User', 'user@system.local', 0),
            ('guest', 'guest', 'Guest User', 'guest@system.local', 0)
        ]
        
        for username, password, full_name, email, is_admin in default_users:
            hashed_pw = self.hash_password(password)
            self.cursor.execute('''
                INSERT OR IGNORE INTO users (username, password, full_name, email, is_admin)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, hashed_pw, full_name, email, is_admin))
            
    def authenticate_user(self, username, password):
        """Authenticate user credentials"""
        hashed_pw = self.hash_password(password)
        self.cursor.execute('''
            SELECT id FROM users WHERE username = ? AND password = ?
        ''', (username, hashed_pw))
        return self.cursor.fetchone() is not None
        
    def get_users(self):
        """Get list of all users"""
        self.cursor.execute('SELECT username FROM users ORDER BY username')
        return [row[0] for row in self.cursor.fetchall()]
        
    def update_last_login(self, username):
        """Update user's last login time"""
        self.cursor.execute('''
            UPDATE users SET last_login = CURRENT_TIMESTAMP 
            WHERE username = ?
        ''', (username,))
        self.connection.commit()
        
    def get_setting(self, key, default=None):
        """Get system setting"""
        self.cursor.execute('''
            SELECT setting_value FROM settings 
            WHERE user_id IS NULL AND setting_key = ?
        ''', (key,))
        result = self.cursor.fetchone()
        return result[0] if result else default
        
    def set_setting(self, key, value):
        """Set system setting"""
        self.cursor.execute('''
            INSERT OR REPLACE INTO settings (user_id, setting_key, setting_value)
            VALUES (NULL, ?, ?)
        ''', (key, value))
        self.connection.commit()

   def get_system_info(self, key, default=None):
        """Get system information"""
        self.cursor.execute('SELECT value FROM system_info WHERE key = ?', (key,))
        result = self.cursor.fetchone()
        return result[0] if result else default
        
   def set_system_info(self, key, value):
        """Set system information"""
        self.cursor.execute('''
            INSERT OR REPLACE INTO system_info (key, value)
            VALUES (?, ?)
        ''', (key, value))
        self.connection.commit()
