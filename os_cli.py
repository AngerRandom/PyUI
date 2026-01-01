# os_cli.py - Command Line Interface for Python OS Simulator
import argparse
import sys
import os
import sqlite3
import json
from datetime import datetime
import getpass
import hashlib

class OSCLI:
    def __init__(self):
        self.db_path = 'system.db'
        self.setup_wizard_enabled = False
        self.init_database_connection()
        
    def init_database_connection(self):
        """Initialize database connection"""
        try:
            # Check if database exists
            if not os.path.exists(self.db_path):
                print(f"Error: Database '{self.db_path}' not found.")
                print("Make sure the OS Simulator has been run at least once.")
                sys.exit(1)
                
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            self.cursor = self.conn.cursor()
            print(f"Connected to database: {self.db_path}")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            sys.exit(1)
            
    def hash_password(self, password):
        """Hash password for storage"""
        return hashlib.sha256(password.encode()).hexdigest()
        
    def run(self):
        """Main CLI entry point"""
        parser = argparse.ArgumentParser(
            description='Python OS Simulator CLI Management Tool',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''
Examples:
  %(prog)s reset-system               # Reset system and trigger setup wizard
  %(prog)s user --list                # List all users
  %(prog)s user --add john            # Add new user 'john'
  %(prog)s user --delete admin        # Delete user 'admin'
  %(prog)s reset-settings             # Reset all settings to default
  %(prog)s status                     # Show system status
  %(prog)s backup --output backup.db  # Backup system database
            '''
        )
        
        # Create subparsers for different commands
        subparsers = parser.add_subparsers(dest='command', help='Command to execute')
        
        # Reset system command
        reset_parser = subparsers.add_parser('reset-system', 
                                           help='Reset system and trigger setup wizard')
        reset_parser.add_argument('--force', action='store_true',
                                help='Force reset without confirmation')
        
        # User management command
        user_parser = subparsers.add_parser('user', help='User management')
        user_group = user_parser.add_mutually_exclusive_group(required=True)
        user_group.add_argument('--list', action='store_true', help='List all users')
        user_group.add_argument('--add', metavar='USERNAME', help='Add new user')
        user_group.add_argument('--delete', metavar='USERNAME', help='Delete user')
        user_group.add_argument('--modify', metavar='USERNAME', help='Modify user')
        user_group.add_argument('--reset-password', metavar='USERNAME', 
                              help='Reset user password')
        user_parser.add_argument('--admin', action='store_true',
                               help='Make user administrator (for --add/--modify)')
        user_parser.add_argument('--name', help='Full name for user')
        user_parser.add_argument('--email', help='Email for user')
        
        # Settings reset command
        settings_parser = subparsers.add_parser('reset-settings', 
                                              help='Reset all settings to default')
        settings_parser.add_argument('--force', action='store_true',
                                   help='Force reset without confirmation')
        
        # Status command
        status_parser = subparsers.add_parser('status', help='Show system status')
        
        # Backup command
        backup_parser = subparsers.add_parser('backup', help='Backup system')
        backup_parser.add_argument('--output', default='backup.db',
                                 help='Output backup file name')
        backup_parser.add_argument('--compress', action='store_true',
                                 help='Compress backup file')
        
        # Restore command
        restore_parser = subparsers.add_parser('restore', help='Restore system from backup')
        restore_parser.add_argument('--input', required=True,
                                  help='Input backup file name')
        restore_parser.add_argument('--force', action='store_true',
                                  help='Force restore without confirmation')
        
        # Log command
        log_parser = subparsers.add_parser('logs', help='View system logs')
        log_parser.add_argument('--type', choices=['system', 'login', 'error', 'all'],
                              default='all', help='Type of logs to view')
        log_parser.add_argument('--limit', type=int, default=50,
                              help='Number of log entries to show')
        log_parser.add_argument('--tail', action='store_true',
                              help='Show only recent logs')
        
        # Filesystem command
        fs_parser = subparsers.add_parser('filesystem', help='Manage virtual filesystem')
        fs_subparsers = fs_parser.add_subparsers(dest='fs_command', help='Filesystem command')
        
        # List files
        fs_list_parser = fs_subparsers.add_parser('list', help='List files')
        fs_list_parser.add_argument('path', nargs='?', default='/',
                                  help='Path to list')
        
        # Create file/directory
        fs_create_parser = fs_subparsers.add_parser('create', help='Create file or directory')
        fs_create_parser.add_argument('path', help='Path to create')
        fs_create_parser.add_argument('--type', choices=['file', 'directory'],
                                    required=True, help='Type to create')
        fs_create_parser.add_argument('--content', help='Content for file')
        
        # Delete file/directory
        fs_delete_parser = fs_subparsers.add_parser('delete', help='Delete file or directory')
        fs_delete_parser.add_argument('path', help='Path to delete')
        fs_delete_parser.add_argument('--force', action='store_true',
                                    help='Force deletion')
        
        # System info command
        info_parser = subparsers.add_parser('info', help='Show detailed system information')
        
        # Update command
        update_parser = subparsers.add_parser('update', help='Check for system updates')
        update_parser.add_argument('--install', action='store_true',
                                 help='Install available updates')
        
        # Repair command
        repair_parser = subparsers.add_parser('repair', help='Repair system database')
        repair_parser.add_argument('--check', action='store_true',
                                 help='Check for issues without repairing')
        
        # Parse arguments
        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(1)
            
        args = parser.parse_args()
        
        # Execute command
        if args.command == 'reset-system':
            self.reset_system(args.force)
        elif args.command == 'user':
            self.manage_user(args)
        elif args.command == 'reset-settings':
            self.reset_settings(args.force)
        elif args.command == 'status':
            self.show_status()
        elif args.command == 'backup':
            self.backup_system(args.output, args.compress)
        elif args.command == 'restore':
            self.restore_system(args.input, args.force)
        elif args.command == 'logs':
            self.view_logs(args.type, args.limit, args.tail)
        elif args.command == 'filesystem':
            self.manage_filesystem(args)
        elif args.command == 'info':
            self.show_system_info()
        elif args.command == 'update':
            self.check_updates(args.install)
        elif args.command == 'repair':
            self.repair_database(args.check)
        else:
            parser.print_help()
            
    def reset_system(self, force=False):
        """Reset system and trigger setup wizard"""
        print("=" * 60)
        print("SYSTEM RESET")
        print("=" * 60)
        
        if not force:
            print("\n⚠️  WARNING: This will reset the entire system!")
            print("The following actions will be performed:")
            print("1. Reset setup wizard flag (will run setup on next boot)")
            print("2. Remove all user settings")
            print("3. Reset system preferences")
            print("4. Clear application data")
            print("5. Preserve user accounts (optional)")
            
            confirm = input("\nAre you sure you want to continue? (yes/NO): ").strip().lower()
            if confirm not in ['yes', 'y']:
                print("Reset cancelled.")
                return
                
        print("\nStarting system reset...")
        
        try:
            # Reset setup completion flag
            self.cursor.execute("DELETE FROM system_info WHERE key = 'setup_completed'")
            self.cursor.execute("INSERT INTO system_info (key, value) VALUES (?, ?)",
                              ('setup_completed', 'false'))
            
            # Reset all user settings
            self.cursor.execute("DELETE FROM settings")
            
            # Reset theme to default
            self.cursor.execute('''
                INSERT INTO settings (user_id, setting_key, setting_value)
                SELECT id, 'theme', 'default' FROM users WHERE username = 'admin'
            ''')
            
            # Clear system log (keep last 100 entries)
            self.cursor.execute('''
                DELETE FROM system_log 
                WHERE id NOT IN (
                    SELECT id FROM system_log 
                    ORDER BY timestamp DESC 
                    LIMIT 100
                )
            ''')
            
            # Reset computer name
            self.cursor.execute("DELETE FROM system_info WHERE key = 'computer_name'")
            self.cursor.execute("INSERT INTO system_info (key, value) VALUES (?, ?)",
                              ('computer_name', 'PythonOS-PC'))
            
            # Reset timezone
            self.cursor.execute("DELETE FROM system_info WHERE key = 'timezone'")
            self.cursor.execute("INSERT INTO system_info (key, value) VALUES (?, ?)",
                              ('timezone', 'UTC'))
            
            self.conn.commit()
            
            print("✓ System reset completed successfully!")
            print("\nNext steps:")
            print("1. Start the OS Simulator")
            print("2. The setup wizard will automatically run")
            print("3. Configure your system as new")
            
            # Create a flag file to trigger setup
            with open('reset.flag', 'w') as f:
                f.write(f'Reset performed at: {datetime.now().isoformat()}\n')
                
        except Exception as e:
            print(f"✗ Error during system reset: {e}")
            self.conn.rollback()
            
    def manage_user(self, args):
        """Manage users"""
        if args.list:
            self.list_users()
        elif args.add:
            self.add_user(args.add, args.admin, args.name, args.email)
        elif args.delete:
            self.delete_user(args.delete)
        elif args.modify:
            self.modify_user(args.modify, args.admin, args.name, args.email)
        elif args.reset_password:
            self.reset_password(args.reset_password)
            
    def list_users(self):
        """List all users"""
        print("=" * 60)
        print("USER LIST")
        print("=" * 60)
        
        try:
            self.cursor.execute('''
                SELECT id, username, full_name, email, is_admin, 
                       created_at, last_login
                FROM users 
                ORDER BY username
            ''')
            users = self.cursor.fetchall()
            
            if not users:
                print("No users found.")
                return
                
            print(f"\n{'Username':<15} {'Full Name':<20} {'Admin':<6} {'Last Login':<20}")
            print("-" * 70)
            
            for user in users:
                last_login = user['last_login'] or 'Never'
                if last_login != 'Never':
                    try:
                        last_login = last_login[:19]  # Trim microseconds
                    except:
                        pass
                        
                admin_status = "Yes" if user['is_admin'] else "No"
                print(f"{user['username']:<15} {user['full_name'] or '':<20} "
                      f"{admin_status:<6} {last_login:<20}")
                      
            print(f"\nTotal users: {len(users)}")
            
        except Exception as e:
            print(f"Error listing users: {e}")
            
    def add_user(self, username, is_admin=False, full_name=None, email=None):
        """Add a new user"""
        print(f"\nAdding user: {username}")
        
        # Check if user already exists
        self.cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if self.cursor.fetchone():
            print(f"Error: User '{username}' already exists.")
            return
            
        # Get password
        password = getpass.getpass("Password: ")
        confirm = getpass.getpass("Confirm password: ")
        
        if password != confirm:
            print("Error: Passwords do not match.")
            return
            
        if len(password) < 4:
            print("Error: Password must be at least 4 characters.")
            return
            
        # Get full name if not provided
        if not full_name:
            full_name = input("Full name (optional): ").strip() or None
            
        # Get email if not provided
        if not email:
            email = input("Email (optional): ").strip() or None
            
        try:
            hashed_password = self.hash_password(password)
            
            self.cursor.execute('''
                INSERT INTO users (username, password, full_name, email, is_admin)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, hashed_password, full_name, email, 1 if is_admin else 0))
            
            self.conn.commit()
            
            print(f"✓ User '{username}' added successfully!")
            if is_admin:
                print("  Administrator privileges granted.")
                
        except Exception as e:
            print(f"✗ Error adding user: {e}")
            self.conn.rollback()
            
    def delete_user(self, username):
        """Delete a user"""
        # Prevent deleting the last admin user
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1")
        admin_count = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT is_admin FROM users WHERE username = ?", (username,))
        user = self.cursor.fetchone()
        
        if not user:
            print(f"Error: User '{username}' not found.")
            return
            
        if user['is_admin'] and admin_count <= 1:
            print("Error: Cannot delete the last administrator user.")
            return
            
        confirm = input(f"Are you sure you want to delete user '{username}'? (yes/NO): ")
        if confirm.lower() not in ['yes', 'y']:
            print("Deletion cancelled.")
            return
            
        try:
            # Get user ID
            self.cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            user_id = self.cursor.fetchone()[0]
            
            # Delete user settings
            self.cursor.execute("DELETE FROM settings WHERE user_id = ?", (user_id,))
            
            # Delete user
            self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            
            self.conn.commit()
            print(f"✓ User '{username}' deleted successfully!")
            
        except Exception as e:
            print(f"✗ Error deleting user: {e}")
            self.conn.rollback()
            
    def modify_user(self, username, is_admin=None, full_name=None, email=None):
        """Modify user properties"""
        # Check if user exists
        self.cursor.execute("SELECT id, is_admin FROM users WHERE username = ?", (username,))
        user = self.cursor.fetchone()
        
        if not user:
            print(f"Error: User '{username}' not found.")
            return
            
        print(f"\nModifying user: {username}")
        
        # Check if trying to remove last admin
        if is_admin is False and user['is_admin']:
            self.cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1")
            admin_count = self.cursor.fetchone()[0]
            
            if admin_count <= 1:
                print("Error: Cannot remove admin privileges from the last administrator.")
                return
                
        updates = []
        params = []
        
        if is_admin is not None:
            updates.append("is_admin = ?")
            params.append(1 if is_admin else 0)
            
        if full_name is not None:
            updates.append("full_name = ?")
            params.append(full_name)
            
        if email is not None:
            updates.append("email = ?")
            params.append(email)
            
        if not updates:
            print("No changes specified.")
            return
            
        params.append(username)  # For WHERE clause
        
        try:
            query = f"UPDATE users SET {', '.join(updates)} WHERE username = ?"
            self.cursor.execute(query, params)
            
            self.conn.commit()
            print(f"✓ User '{username}' modified successfully!")
            
        except Exception as e:
            print(f"✗ Error modifying user: {e}")
            self.rollback()
            
    def reset_password(self, username):
        """Reset user password"""
        # Check if user exists
        self.cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if not self.cursor.fetchone():
            print(f"Error: User '{username}' not found.")
            return
            
        print(f"\nResetting password for user: {username}")
        
        password = getpass.getpass("New password: ")
        confirm = getpass.getpass("Confirm new password: ")
        
        if password != confirm:
            print("Error: Passwords do not match.")
            return
            
        if len(password) < 4:
            print("Error: Password must be at least 4 characters.")
            return
            
        try:
            hashed_password = self.hash_password(password)
            
            self.cursor.execute('''
                UPDATE users SET password = ? WHERE username = ?
            ''', (hashed_password, username))
            
            self.conn.commit()
            print(f"✓ Password for user '{username}' reset successfully!")
            
        except Exception as e:
            print(f"✗ Error resetting password: {e}")
            self.conn.rollback()
            
    def reset_settings(self, force=False):
        """Reset all settings to default"""
        print("=" * 60)
        print("SETTINGS RESET")
        print("=" * 60)
        
        if not force:
            print("\n⚠️  WARNING: This will reset all user and system settings!")
            print("The following will be reset to defaults:")
            print("1. All user preferences")
            print("2. System configuration")
            print("3. Application settings")
            
            confirm = input("\nAre you sure you want to continue? (yes/NO): ").strip().lower()
            if confirm not in ['yes', 'y']:
                print("Reset cancelled.")
                return
                
        print("\nResetting settings...")
        
        try:
            # Delete all settings
            self.cursor.execute("DELETE FROM settings")
            
            # Set default settings for admin user
            admin_id = self.get_admin_id()
            if admin_id:
                default_settings = [
                    (admin_id, 'theme', 'default'),
                    (admin_id, 'wallpaper', 'Default'),
                    (admin_id, 'sound_enabled', 'true'),
                    (admin_id, 'sound_volume', '0.7'),
                    (admin_id, 'auto_update', 'true'),
                    (admin_id, 'privacy_reporting', 'true')
                ]
                
                for setting in default_settings:
                    self.cursor.execute('''
                        INSERT INTO settings (user_id, setting_key, setting_value)
                        VALUES (?, ?, ?)
                    ''', setting)
                    
            # Reset system info defaults
            defaults = [
                ('computer_name', 'PythonOS-PC'),
                ('timezone', 'UTC'),
                ('auto_login', 'false')
            ]
            
            for key, value in defaults:
                self.cursor.execute('''
                    INSERT OR REPLACE INTO system_info (key, value)
                    VALUES (?, ?)
                ''', (key, value))
                
            self.conn.commit()
            print("✓ All settings reset to defaults!")
            
        except Exception as e:
            print(f"✗ Error resetting settings: {e}")
            self.conn.rollback()
            
    def get_admin_id(self):
        """Get admin user ID"""
        self.cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        result = self.cursor.fetchone()
        return result[0] if result else None
        
    def show_status(self):
        """Show system status"""
        print("=" * 60)
        print("SYSTEM STATUS")
        print("=" * 60)
        
        try:
            # Get basic statistics
            stats = {}
            
            # User count
            self.cursor.execute("SELECT COUNT(*) FROM users")
            stats['users'] = self.cursor.fetchone()[0]
            
            # Admin count
            self.cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1")
            stats['admins'] = self.cursor.fetchone()[0]
            
            # Log entries
            self.cursor.execute("SELECT COUNT(*) FROM system_log")
            stats['logs'] = self.cursor.fetchone()[0]
            
            # Filesystem items
            self.cursor.execute("SELECT COUNT(*) FROM filesystem")
            stats['files'] = self.cursor.fetchone()[0]
            
            # Settings count
            self.cursor.execute("SELECT COUNT(*) FROM settings")
            stats['settings'] = self.cursor.fetchone()[0]
            
            # Installed apps
            self.cursor.execute("SELECT COUNT(*) FROM installed_apps")
            stats['apps'] = self.cursor.fetchone()[0]
            
            # System info
            self.cursor.execute("SELECT key, value FROM system_info")
            system_info = {row['key']: row['value'] for row in self.cursor.fetchall()}
            
            print("\n📊 Statistics:")
            print(f"  Users: {stats['users']} ({stats['admins']} administrators)")
            print(f"  Log entries: {stats['logs']}")
            print(f"  Files: {stats['files']}")
            print(f"  Settings: {stats['settings']}")
            print(f"  Installed apps: {stats['apps']}")
            
            print("\n⚙️  System Information:")
            print(f"  Setup completed: {'Yes' if system_info.get('setup_completed') == 'true' else 'No'}")
            print(f"  Computer name: {system_info.get('computer_name', 'Not set')}")
            print(f"  Timezone: {system_info.get('timezone', 'Not set')}")
            print(f"  Version: {system_info.get('version', 'Unknown')}")
            print(f"  Build: {system_info.get('build', 'Unknown')}")
            
            # Database size
            db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
            print(f"  Database size: {db_size / 1024:.1f} KB")
            
            # Last log entry
            self.cursor.execute('''
                SELECT event_type, timestamp 
                FROM system_log 
                ORDER BY timestamp DESC 
                LIMIT 1
            ''')
            last_log = self.cursor.fetchone()
            if last_log:
                print(f"\n📝 Last system event:")
                print(f"  Type: {last_log['event_type']}")
                print(f"  Time: {last_log['timestamp']}")
                
            print("\n✅ System is operational.")
            
        except Exception as e:
            print(f"Error getting status: {e}")
            
    def backup_system(self, output_file, compress=False):
        """Backup system database"""
        print("=" * 60)
        print("SYSTEM BACKUP")
        print("=" * 60)
        
        try:
            # Check if output file already exists
            if os.path.exists(output_file):
                confirm = input(f"File '{output_file}' already exists. Overwrite? (yes/NO): ")
                if confirm.lower() not in ['yes', 'y']:
                    print("Backup cancelled.")
                    return
                    
            # Create backup
            import shutil
            shutil.copy2(self.db_path, output_file)
            
            # Compress if requested
            if compress:
                import gzip
                with open(output_file, 'rb') as f_in:
                    with gzip.open(f"{output_file}.gz", 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(output_file)
                output_file = f"{output_file}.gz"
                
            size = os.path.getsize(output_file)
            print(f"\n✓ Backup created successfully!")
            print(f"  File: {output_file}")
            print(f"  Size: {size / 1024:.1f} KB")
            print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            print(f"✗ Error creating backup: {e}")
            
    def restore_system(self, input_file, force=False):
        """Restore system from backup"""
        print("=" * 60)
        print("SYSTEM RESTORE")
        print("=" * 60)
        
        if not os.path.exists(input_file):
            print(f"Error: Backup file '{input_file}' not found.")
            return
            
        if not force:
            print("\n⚠️  WARNING: This will overwrite the current system!")
            print("All current data will be replaced with the backup.")
            
            confirm = input("\nAre you sure you want to continue? (yes/NO): ").strip().lower()
            if confirm not in ['yes', 'y']:
                print("Restore cancelled.")
                return
                
        try:
            # Check if database is in use
            try:
                self.conn.close()
            except:
                pass
                
            # Handle compressed backup
            if input_file.endswith('.gz'):
                import gzip
                import tempfile
                
                with gzip.open(input_file, 'rb') as f_in:
                    with tempfile.NamedTemporaryFile(delete=False) as tmp:
                        shutil.copyfileobj(f_in, tmp)
                        temp_path = tmp.name
                        
                shutil.copy2(temp_path, self.db_path)
                os.remove(temp_path)
            else:
                shutil.copy2(input_file, self.db_path)
                
            print(f"\n✓ System restored successfully from '{input_file}'!")
            print("Restart the OS Simulator to use the restored system.")
            
            # Reconnect to database
            self.init_database_connection()
            
        except Exception as e:
            print(f"✗ Error restoring system: {e}")
            
    def view_logs(self, log_type, limit, tail):
        """View system logs"""
        print("=" * 60)
        print("SYSTEM LOGS")
        print("=" * 60)
        
        try:
            query = "SELECT id, event_type, event_data, timestamp FROM system_log"
            params = []
            
            if log_type != 'all':
                if log_type == 'login':
                    query += " WHERE event_type LIKE '%login%'"
                elif log_type == 'error':
                    query += " WHERE severity = 'error' OR event_type LIKE '%error%'"
                    
            if tail:
                query += " ORDER BY timestamp DESC LIMIT ?"
                params.append(limit)
            else:
                query += " ORDER BY timestamp LIMIT ?"
                params.append(limit)
                
            self.cursor.execute(query, params)
            logs = self.cursor.fetchall()
            
            if not logs:
                print("\nNo logs found.")
                return
                
            print(f"\nShowing {len(logs)} log entries:")
            print("-" * 100)
            
            for log in logs:
                event_data = log['event_data']
                try:
                    if event_data:
                        data = json.loads(event_data)
                        data_str = json.dumps(data, indent=2)
                    else:
                        data_str = ""
                except:
                    data_str = event_data or ""
                    
                print(f"\n[{log['timestamp']}] {log['event_type']}")
                if data_str:
                    for line in data_str.split('\n'):
                        if line:
                            print(f"  {line}")
                            
            print("\n" + "-" * 100)
            print(f"Total logs shown: {len(logs)}")
            
        except Exception as e:
            print(f"Error viewing logs: {e}")
            
    def manage_filesystem(self, args):
        """Manage virtual filesystem"""
        if args.fs_command == 'list':
            self.list_files(args.path)
        elif args.fs_command == 'create':
            self.create_fs_item(args.path, args.type, args.content)
        elif args.fs_command == 'delete':
            self.delete_fs_item(args.path, args.force)
            
    def list_files(self, path):
        """List files in virtual filesystem"""
        print(f"\nListing: {path}")
        print("-" * 60)
        
        try:
            self.cursor.execute('''
                SELECT name, type, size, modified_at, owner, permissions
                FROM filesystem 
                WHERE path = ?
                ORDER BY type DESC, name
            ''', (path,))
            
            items = self.cursor.fetchall()
            
            if not items:
                print("Directory is empty.")
                return
                
            print(f"{'Type':<4} {'Permissions':<10} {'Size':<8} {'Modified':<19} {'Name'}")
            print("-" * 60)
            
            for item in items:
                item_type = 'd' if item['type'] == 'directory' else '-'
                size = f"{item['size']}" if item['size'] else "0"
                modified = item['modified_at'][:19] if item['modified_at'] else ""
                
                print(f"{item_type:<4} {item['permissions']:<10} {size:<8} "
                      f"{modified:<19} {item['name']}")
                      
            print(f"\nTotal items: {len(items)}")
            
        except Exception as e:
            print(f"Error listing files: {e}")
            
    def create_fs_item(self, path, item_type, content=None):
        """Create file or directory in virtual filesystem"""
        import os.path as op
        
        # Extract directory and name from path
        dir_path = op.dirname(path)
        name = op.basename(path)
        
        if not name:
            print("Error: Invalid path.")
            return
            
        # Check if parent directory exists
        self.cursor.execute('''
            SELECT id FROM filesystem 
            WHERE path = ? AND name = ? AND type = 'directory'
        ''', (op.dirname(dir_path), op.basename(dir_path)))
        
        # For simplicity, we'll just create it
        print(f"Creating {item_type}: {path}")
        
        try:
            size = len(content) if content else 0
            
            self.cursor.execute('''
                INSERT INTO filesystem (name, type, path, content, size)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, item_type, dir_path, content, size))
            
            self.conn.commit()
            print(f"✓ Created {item_type} '{path}' successfully!")
            
        except Exception as e:
            print(f"✗ Error creating {item_type}: {e}")
            self.conn.rollback()
            
    def delete_fs_item(self, path, force=False):
        """Delete file or directory"""
        import os.path as op
        
        dir_path = op.dirname(path)
        name = op.basename(path)
        
        # Check if item exists
        self.cursor.execute('''
            SELECT type FROM filesystem 
            WHERE path = ? AND name = ?
        ''', (dir_path, name))
        
        item = self.cursor.fetchone()
        if not item:
            print(f"Error: '{path}' not found.")
            return
            
        # Check if directory is not empty
        if item['type'] == 'directory' and not force:
            self.cursor.execute('''
                SELECT COUNT(*) FROM filesystem 
                WHERE path = ?
            ''', (path,))
            
            count = self.cursor.fetchone()[0]
            if count > 0:
                confirm = input(f"Directory '{path}' is not empty. Delete recursively? (yes/NO): ")
                if confirm.lower() not in ['yes', 'y']:
                    print("Deletion cancelled.")
                    return
                    
        confirm = input(f"Are you sure you want to delete '{path}'? (yes/NO): ")
        if confirm.lower() not in ['yes', 'y']:
            print("Deletion cancelled.")
            return
            
        try:
            # Delete item
            self.cursor.execute('''
                DELETE FROM filesystem 
                WHERE path = ? AND name = ?
            ''', (dir_path, name))
            
            # If directory, delete contents too
            if item['type'] == 'directory':
                self.cursor.execute('''
                    DELETE FROM filesystem 
                    WHERE path LIKE ? || '%'
                ''', (path,))
                
            self.conn.commit()
            print(f"✓ Deleted '{path}' successfully!")
            
        except Exception as e:
            print(f"✗ Error deleting: {e}")
            self.conn.rollback()
            
    def show_system_info(self):
        """Show detailed system information"""
        print("=" * 60)
        print("SYSTEM INFORMATION")
        print("=" * 60)
        
        try:
            # Get all system info
            self.cursor.execute("SELECT key, value FROM system_info ORDER BY key")
            system_info = self.cursor.fetchall()
            
            print("\n🔧 System Configuration:")
            for info in system_info:
                print(f"  {info['key']:<20}: {info['value']}")
                
            # Get database info
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = self.cursor.fetchall()
            
            print(f"\n🗃️  Database Information:")
            print(f"  Tables: {len(tables)}")
            for table in tables:
                self.cursor.execute(f"SELECT COUNT(*) FROM {table['name']}")
                count = self.cursor.fetchone()[0]
                print(f"    {table['name']:<20}: {count} rows")
                
            # Get Python and OS info
            import platform
            print(f"\n💻 Environment:")
            print(f"  Python: {platform.python_version()}")
            print(f"  OS: {platform.system()} {platform.release()}")
            print(f"  Processor: {platform.processor() or 'Unknown'}")
            
            # Disk space
            import shutil
            total, used, free = shutil.disk_usage(".")
            print(f"\n💾 Disk Space:")
            print(f"  Total: {total // (2**30)} GB")
            print(f"  Used: {used // (2**30)} GB")
            print(f"  Free: {free // (2**30)} GB")
            
        except Exception as e:
            print(f"Error getting system info: {e}")
            
    def check_updates(self, install=False):
        """Check for system updates"""
        print("=" * 60)
        print("SYSTEM UPDATES")
        print("=" * 60)
        
        print("\nChecking for updates...")
        
        # Simulated update check
        import random
        has_updates = random.choice([True, False])
        
        if has_updates:
            print("✓ Updates available!")
            print("\nAvailable updates:")
            print("  • Python OS Core v2.0 → v2.1")
            print("  • Security Patch 2024-01")
            print("  • Application updates (3 packages)")
            
            if install:
                print("\nInstalling updates...")
                # Simulated installation
                import time
                for i in range(1, 6):
                    print(f"  Installing update {i}/5...")
                    time.sleep(0.5)
                print("\n✓ Updates installed successfully!")
                print("Restart the OS Simulator to apply updates.")
            else:
                print("\nRun 'os_cli.py update --install' to install updates.")
        else:
            print("✓ System is up to date!")
            
    def repair_database(self, check_only=False):
        """Repair system database"""
        print("=" * 60)
        print("DATABASE REPAIR")
        print("=" * 60)
        
        print("\nChecking database integrity...")
        
        try:
            # Check integrity
            self.cursor.execute("PRAGMA integrity_check")
            result = self.cursor.fetchone()[0]
            
            if result == "ok":
                print("✓ Database integrity check passed.")
                
                if not check_only:
                    # Optimize database
                    print("\nOptimizing database...")
                    self.cursor.execute("VACUUM")
                    self.conn.commit()
                    print("✓ Database optimized successfully!")
            else:
                print(f"✗ Database issues found: {result}")
                
                if not check_only:
                    confirm = input("\nAttempt to repair database? (yes/NO): ")
                    if confirm.lower() in ['yes', 'y']:
                        print("Repairing database...")
                        # Backup first
                        backup_file = f"repair_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                        shutil.copy2(self.db_path, backup_file)
                        print(f"  Backup created: {backup_file}")
                        
                        # Try to repair
                        try:
                            self.cursor.execute("REINDEX")
                            self.cursor.execute("VACUUM")
                            self.conn.commit()
                            print("✓ Database repair attempted.")
                            print("  Note: Some data may be lost. Check the backup.")
                        except Exception as e:
                            print(f"✗ Repair failed: {e}")
                            
        except Exception as e:
            print(f"Error during repair: {e}")

def main():
    """Main entry point"""
    cli = OSCLI()
    cli.run()

if __name__ == "__main__":
    main()