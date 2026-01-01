# main.py - Extended with new features
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import json
import os
import sys
import logging
from datetime import datetime
import pygame
from PIL import Image, ImageTk
import time
import threading
import importlib.util
import subprocess
import traceback

# Import modules
from database import DatabaseManager
from desktop import Desktop
from themes.theme_manager import ThemeManager
from window_manager import WindowManager
from crash_handler import CrashHandler
from package_manager import PackageManager

class OSSimulator:
    def __init__(self):
        # Initialize logging
        self.setup_logging()
        
        # Initialize pygame for sound
        pygame.mixer.init()
        
        # Initialize database
        self.db = DatabaseManager()
        self.db.init_database()
        
        # Initialize theme manager
        self.theme_manager = ThemeManager()
        
        # Initialize window manager
        self.window_manager = WindowManager()
        
        # Initialize crash handler
        self.crash_handler = CrashHandler(self)
        
        # Initialize package manager
        self.package_manager = PackageManager(self)
        
        # Initialize main window
        self.root = tk.Tk()
        self.root.title("Python OS Simulator")
        self.root.geometry("1024x768")
        self.root.configure(bg='black')
        
        # Register with window manager
        self.window_manager.register_window('main', self.root)
        
        # Set fullscreen option
        self.fullscreen = False
        
        # Current user
        self.current_user = None
        
        # System state
        self.system_state = 'booting'
        self.restart_pending = False
        
        # Installed applications
        self.installed_apps = self.load_installed_apps()
        
        # Boot screen
        self.show_boot_screen()
        
    def setup_logging(self):
        """Setup logging system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('system.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("OS Simulator initialized")
        
    def load_installed_apps(self):
        """Load installed applications from database"""
        try:
            self.db.connect()
            self.db.cursor.execute('''
                CREATE TABLE IF NOT EXISTS installed_apps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    version TEXT,
                    author TEXT,
                    description TEXT,
                    entry_point TEXT,
                    icon_path TEXT,
                    category TEXT,
                    installed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.db.connection.commit()
            
            # Load default apps
            default_apps = [
                ('Terminal', '1.0', 'System', 'Command line interface', 
                 'applications.terminal.TerminalApp', None, 'System'),
                ('File Explorer', '1.0', 'System', 'File management', 
                 'applications.file_explorer.FileExplorer', None, 'System'),
                ('Paint', '1.0', 'System', 'Drawing application', 
                 'applications.paint.PaintApp', None, 'Graphics'),
                ('Media Player', '1.0', 'System', 'Media playback', 
                 'applications.media_player.MediaPlayer', None, 'Multimedia'),
                ('Settings', '1.0', 'System', 'System settings', 
                 'applications.settings.SettingsApp', None, 'System'),
                ('Web Browser', '1.0', 'System', 'Internet browser', 
                 'applications.browser.Browser', None, 'Internet'),
                ('Package Manager', '1.0', 'System', 'Application installer', 
                 'applications.package_manager.PackageManagerApp', None, 'System'),
            ]
            
            for app in default_apps:
                self.db.cursor.execute('''
                    INSERT OR IGNORE INTO installed_apps 
                    (name, version, author, description, entry_point, icon_path, category)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', app)
            self.db.connection.commit()
            
            # Get all installed apps
            self.db.cursor.execute('SELECT name, entry_point, icon_path FROM installed_apps')
            return {row[0]: {'entry_point': row[1], 'icon': row[2]} for row in self.db.cursor.fetchall()}
            
        except Exception as e:
            self.logger.error(f"Error loading installed apps: {e}")
            return {}
            
    def show_boot_screen(self):
        """Display boot animation"""
        self.logger.info("Showing boot screen")
        self.system_state = 'booting'
        
        self.boot_frame = tk.Frame(self.root, bg='black')
        self.boot_frame.pack(fill=tk.BOTH, expand=True)
        
        # Manufacturer logo
        logo_label = tk.Label(
            self.boot_frame,
            text="PYTHON\nOS\nSIMULATOR",
            font=('Courier', 32, 'bold'),
            fg='#00ff00',
            bg='black',
            justify=tk.CENTER
        )
        logo_label.pack(pady=100)
        
        # Version info
        version_label = tk.Label(
            self.boot_frame,
            text="Version 2.0\n© 2024 Python OS Project",
            font=('Courier', 10),
            fg='#888888',
            bg='black',
            justify=tk.CENTER
        )
        version_label.pack(pady=20)
        
        # Progress bar
        self.boot_progress = ttk.Progressbar(
            self.boot_frame,
            mode='determinate',
            length=400,
            style="green.Horizontal.TProgressbar"
        )
        self.boot_progress.pack(pady=20)
        
        # Boot messages
        self.boot_text = tk.Text(
            self.boot_frame,
            height=8,
            width=70,
            bg='black',
            fg='#00ff00',
            font=('Courier', 9),
            highlightthickness=0,
            borderwidth=0
        )
        self.boot_text.pack(pady=20)
        self.boot_text.insert(tk.END, "[   0.000000] Initializing kernel...\n")
        
        # Simulate boot process
        self.root.after(1000, self.simulate_boot)
        
    def simulate_boot(self):
        """Simulate boot process with messages"""
        boot_messages = [
            (0.5, "[   0.502345] Setting up system architecture..."),
            (1.2, "[   1.702891] Initializing memory management..."),
            (2.1, "[   3.812345] Loading drivers..."),
            (3.0, "[   6.812890] Mounting filesystems..."),
            (3.8, "[  10.612345] Starting system services..."),
            (4.5, "[  15.112890] Loading window manager..."),
            (5.2, "[  20.312345] Starting desktop environment..."),
            (5.8, "[  26.112890] Initializing user session..."),
            (6.0, "[  32.112345] System ready for login...")
        ]
        
        def update_boot(index=0, last_time=0):
            if index < len(boot_messages):
                time_offset, message = boot_messages[index]
                delay = int((time_offset - last_time) * 1000)
                
                def show_message():
                    self.boot_text.insert(tk.END, f"{message}\n")
                    self.boot_text.see(tk.END)
                    self.boot_progress['value'] = (index + 1) * (100 / len(boot_messages))
                    update_boot(index + 1, time_offset)
                
                self.root.after(delay, show_message)
            else:
                self.root.after(1000, self.show_login_screen)
        
        update_boot()
        
    def show_login_screen(self):
        """Display login screen"""
        self.logger.info("Showing login screen")
        self.system_state = 'login'
        
        # Clear boot screen
        self.boot_frame.destroy()
        
        # Login frame
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(fill=tk.BOTH, expand=True)
        
        # Apply theme
        theme = self.theme_manager.get_current_theme()
        self.login_frame.config(bg=theme['background'])
        
        # Center container
        center_frame = tk.Frame(
            self.login_frame,
            bg=theme['panel_bg'],
            relief=tk.RAISED,
            borderwidth=2,
            padx=50,
            pady=50
        )
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Logo/Title
        title_label = tk.Label(
            center_frame,
            text="Python OS",
            font=('Arial', 32, 'bold'),
            fg=theme['accent'],
            bg=theme['panel_bg']
        )
        title_label.pack(pady=(0, 30))
        
        # User selection
        users = self.db.get_users()
        self.user_var = tk.StringVar(value=users[0] if users else 'admin')
        
        user_frame = tk.Frame(center_frame, bg=theme['panel_bg'])
        user_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            user_frame,
            text="User:",
            font=('Arial', 12),
            fg=theme['foreground'],
            bg=theme['panel_bg'],
            width=10,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        user_combo = ttk.Combobox(
            user_frame,
            textvariable=self.user_var,
            values=users,
            state='readonly',
            width=20
        )
        user_combo.pack(side=tk.LEFT)
        
        # Password
        pass_frame = tk.Frame(center_frame, bg=theme['panel_bg'])
        pass_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            pass_frame,
            text="Password:",
            font=('Arial', 12),
            fg=theme['foreground'],
            bg=theme['panel_bg'],
            width=10,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        self.password_entry = tk.Entry(
            pass_frame,
            font=('Arial', 12),
            width=22,
            show="●",
            bg=theme['entry_bg'],
            fg=theme['entry_fg'],
            insertbackground=theme['entry_fg']
        )
        self.password_entry.pack(side=tk.LEFT)
        self.password_entry.insert(0, "password")
        
        # Login button
        login_btn = tk.Button(
            center_frame,
            text="Login",
            font=('Arial', 12, 'bold'),
            bg=theme['button_bg'],
            fg=theme['button_fg'],
            padx=30,
            pady=10,
            cursor='hand2',
            command=self.authenticate_user
        )
        login_btn.pack(pady=(10, 0))
        
        # Options
        options_frame = tk.Frame(center_frame, bg=theme['panel_bg'])
        options_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Shutdown button
        shutdown_btn = tk.Button(
            options_frame,
            text="⏻",
            font=('Arial', 14),
            bg=theme['error'],
            fg='white',
            width=3,
            command=self.show_shutdown_screen
        )
        shutdown_btn.pack(side=tk.LEFT, padx=5)
        
        # Restart button
        restart_btn = tk.Button(
            options_frame,
            text="↻",
            font=('Arial', 14),
            bg=theme['warning'],
            fg='white',
            width=3,
            command=self.restart_system
        )
        restart_btn.pack(side=tk.LEFT, padx=5)
        
        # Settings button
        settings_btn = tk.Button(
            options_frame,
            text="⚙",
            font=('Arial', 14),
            bg=theme['accent'],
            fg='white',
            width=3,
            command=self.open_login_settings
        )
        settings_btn.pack(side=tk.LEFT, padx=5)
        
        # Error label
        self.login_error = tk.Label(
            center_frame,
            text="",
            font=('Arial', 10),
            fg=theme['error'],
            bg=theme['panel_bg']
        )
        self.login_error.pack(pady=(10, 0))
        
        # Set focus and bindings
        self.password_entry.focus()
        self.root.bind('<Return>', lambda e: self.authenticate_user())
        
        # Play login sound
        self.play_system_sound('login')
        
    def authenticate_user(self):
        """Authenticate user"""
        username = self.user_var.get()
        password = self.password_entry.get()
        
        if username and password:
            # In real system, verify against database
            success = self.db.authenticate_user(username, password)
            
            self.db.log_event('login_attempt', {
                'username': username,
                'success': success,
                'timestamp': datetime.now().isoformat()
            })
            
            if success:
                self.current_user = username
                self.logger.info(f"User '{username}' logged in successfully")
                
                # Update last login
                self.db.update_last_login(username)
                
                # Play success sound
                self.play_system_sound('login_success')
                
                # Transition to desktop
                self.root.after(500, self.show_desktop)
            else:
                self.login_error.config(text="Invalid username or password")
                self.play_system_sound('error')
        else:
            self.login_error.config(text="Please enter username and password")
            
    def show_desktop(self):
        """Show desktop interface"""
        self.logger.info("Showing desktop")
        self.system_state = 'desktop'
        
        # Clear login screen
        self.login_frame.destroy()
        
        # Create desktop
        self.desktop = Desktop(self.root, self)
        
    def restart_system(self):
        """Restart the system"""
        self.logger.info("System restart requested")
        self.system_state = 'restarting'
        
        # Show restart screen
        self.show_restart_screen()
        
    def show_restart_screen(self):
        """Display restart screen"""
        if hasattr(self, 'login_frame'):
            self.login_frame.destroy()
        
        restart_frame = tk.Frame(self.root, bg='black')
        restart_frame.pack(fill=tk.BOTH, expand=True)
        
        # Restart message
        message_label = tk.Label(
            restart_frame,
            text="Restarting system...",
            font=('Courier', 24),
            fg='white',
            bg='black'
        )
        message_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Animate dots
        dots = [".", "..", "..."]
        
        def animate_restart(index=0):
            if index < 6:  # Animate for 3 seconds
                message_label.config(text=f"Restarting system{dots[index % 3]}")
                self.root.after(500, lambda: animate_restart(index + 1))
            else:
                # Log restart
                self.db.log_event('restart', {
                    'user': self.current_user,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Play restart sound
                self.play_system_sound('restart')
                
                # Simulate restart
                self.root.after(1000, self.simulate_restart)
        
        animate_restart()
        
    def simulate_restart(self):
        """Simulate system restart"""
        # Clear everything
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Show BIOS-like screen
        bios_frame = tk.Frame(self.root, bg='black')
        bios_frame.pack(fill=tk.BOTH, expand=True)
        
        bios_text = tk.Text(
            bios_frame,
            bg='black',
            fg='white',
            font=('Courier', 10),
            highlightthickness=0,
            borderwidth=0
        )
        bios_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        bios_messages = [
            "Python OS BIOS Version 2.0",
            "Copyright (C) 2024 Python OS Project",
            "",
            "Main Processor: Python 3.x",
            "Memory Testing: 16384K OK",
            "",
            "Detecting IDE drives...",
            "IDE Primary Master: SQLite Database",
            "IDE Secondary Master: File System",
            "",
            "Press F2 to enter SETUP, F12 for boot menu",
            "",
            "Booting from primary hard drive...",
            ""
        ]
        
        for msg in bios_messages:
            bios_text.insert(tk.END, msg + "\n")
        
        # Simulate boot delay
        self.root.after(3000, lambda: self.show_boot_screen())
        
    def show_shutdown_screen(self):
        """Display shutdown screen"""
        self.logger.info("Showing shutdown screen")
        self.system_state = 'shutting_down'
        
        # Clear current screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Shutdown frame
        shutdown_frame = tk.Frame(self.root, bg='black')
        shutdown_frame.pack(fill=tk.BOTH, expand=True)
        
        # Shutdown message
        message_label = tk.Label(
            shutdown_frame,
            text="Shutting down...",
            font=('Courier', 24),
            fg='white',
            bg='black'
        )
        message_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        
        # Animate dots
        dots = [".", "..", "..."]
        
        def animate_shutdown(index=0):
            if index < 8:  # Animate for 4 seconds
                message_label.config(text=f"Shutting down{dots[index % 3]}")
                self.root.after(500, lambda: animate_shutdown(index + 1))
            else:
                self.show_safe_to_turn_off()
        
        # Log shutdown
        self.db.log_event('shutdown', {
            'user': self.current_user,
            'timestamp': datetime.now().isoformat()
        })
        
        # Play shutdown sound
        self.play_system_sound('shutdown')
        
        animate_shutdown()
        
    def show_safe_to_turn_off(self):
        """Show 'Safe to turn off your computer' screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        safe_frame = tk.Frame(self.root, bg='black')
        safe_frame.pack(fill=tk.BOTH, expand=True)
        
        # Classic message
        safe_label = tk.Label(
            safe_frame,
            text="It's now safe to turn off\n your computer",
            font=('Courier', 20),
            fg='white',
            bg='black',
            justify=tk.CENTER
        )
        safe_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Option to exit
        exit_btn = tk.Button(
            safe_frame,
            text="Exit Simulator",
            font=('Arial', 12),
            bg='#333333',
            fg='white',
            command=self.root.quit
        )
        exit_btn.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        
        # Option to restart
        restart_btn = tk.Button(
            safe_frame,
            text="Restart",
            font=('Arial', 12),
            bg='#333333',
            fg='white',
            command=self.restart_system
        )
        restart_btn.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
        
    def play_system_sound(self, sound_type):
        """Play system sounds"""
        try:
            if not self.db.get_setting('sound_enabled', 'true') == 'true':
                return
                
            sound_volume = float(self.db.get_setting('sound_volume', '0.7'))
            
            # Generate simple beep sounds if files don't exist
            if sound_type == 'login':
                self.root.bell()
            elif sound_type == 'login_success':
                for _ in range(2):
                    self.root.bell()
                    self.root.after(100)
            elif sound_type == 'error':
                for _ in range(3):
                    self.root.bell()
                    self.root.after(50)
            elif sound_type == 'shutdown':
                for i in range(3, 0, -1):
                    self.root.bell()
                    self.root.after(300)
            elif sound_type == 'restart':
                for _ in range(2):
                    self.root.bell()
                    self.root.after(200)
                    
        except Exception as e:
            self.logger.error(f"Error playing sound: {e}")
            
    def open_login_settings(self):
        """Open settings from login screen"""
        from applications.settings import SettingsApp
        settings = SettingsApp(self.root, self)
        
    def launch_application(self, app_name, *args, **kwargs):
        """Launch an application by name"""
        try:
            if app_name in self.installed_apps:
                entry_point = self.installed_apps[app_name]['entry_point']
                module_name, class_name = entry_point.rsplit('.', 1)
                
                # Import module
                spec = importlib.util.spec_from_file_location(
                    module_name, 
                    f"{module_name.replace('.', '/')}.py"
                )
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                
                # Get class and instantiate
                app_class = getattr(module, class_name)
                app_instance = app_class(self.root, self, *args, **kwargs)
                
                # Register with window manager
                if hasattr(app_instance, 'window'):
                    self.window_manager.register_window(app_name, app_instance.window)
                
                self.logger.info(f"Launched application: {app_name}")
                return app_instance
            else:
                self.logger.error(f"Application not found: {app_name}")
                return None
        except Exception as e:
            self.logger.error(f"Error launching application {app_name}: {e}")
            traceback.print_exc()
            return None
            
    def trigger_crash(self, app_name="Unknown", error_message="System crash"):
        """Trigger a crash screen"""
        self.crash_handler.show_crash_screen(app_name, error_message)
        
    def run(self):
        """Start the OS simulator"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        """Handle window close event"""
        if messagebox.askyesno("Shutdown", "Are you sure you want to shut down?"):
            self.show_shutdown_screen()
        else:
            self.logger.info("Shutdown cancelled")

if __name__ == "__main__":
    app = OSSimulator()
    app.run()