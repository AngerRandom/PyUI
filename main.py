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

# Import modules
from database import DatabaseManager
from desktop import Desktop
from themes.theme_manager import ThemeManager

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
        
        # Initialize main window
        self.root = tk.Tk()
        self.root.title("OS Simulator")
        self.root.geometry("1024x768")
        self.root.configure(bg='black')
        
        # Set fullscreen option (optional)
        self.fullscreen = False
        
        # Current user
        self.current_user = None
        
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
        
    def show_boot_screen(self):
        """Display boot animation"""
        self.logger.info("Showing boot screen")
        
        self.boot_frame = tk.Frame(self.root, bg='black')
        self.boot_frame.pack(fill=tk.BOTH, expand=True)
        
        # Boot logo
        boot_label = tk.Label(
            self.boot_frame,
            text="PYTHON OS SIMULATOR",
            font=('Courier', 24, 'bold'),
            fg='#00ff00',
            bg='black'
        )
        boot_label.pack(pady=200)
        
        # Progress bar
        self.boot_progress = ttk.Progressbar(
            self.boot_frame,
            mode='determinate',
            length=400
        )
        self.boot_progress.pack(pady=20)
        
        # Boot messages
        self.boot_text = tk.Text(
            self.boot_frame,
            height=8,
            width=60,
            bg='black',
            fg='#00ff00',
            font=('Courier', 10)
        )
        self.boot_text.pack(pady=20)
        self.boot_text.insert(tk.END, "Booting system...\n")
        
        # Simulate boot process
        self.root.after(1000, self.simulate_boot)
        
    def simulate_boot(self):
        """Simulate boot process with messages"""
        boot_messages = [
            "Initializing kernel...",
            "Loading drivers...",
            "Mounting filesystems...",
            "Starting services...",
            "Loading desktop environment...",
            "Ready!"
        ]
        
        def update_boot(index=0):
            if index < len(boot_messages):
                message = boot_messages[index]
                self.boot_text.insert(tk.END, f"> {message}\n")
                self.boot_text.see(tk.END)
                self.boot_progress['value'] = (index + 1) * (100 / len(boot_messages))
                self.root.after(500, lambda: update_boot(index + 1))
            else:
                self.root.after(1000, self.show_login_screen)
        
        update_boot()
        
    def show_login_screen(self):
        """Display login screen"""
        self.logger.info("Showing login screen")
        
        # Clear boot screen
        self.boot_frame.destroy()
        
        # Login frame
        self.login_frame = tk.Frame(self.root, bg='#2c3e50')
        self.login_frame.pack(fill=tk.BOTH, expand=True)
        
        # Center container
        center_frame = tk.Frame(self.login_frame, bg='#34495e', padx=40, pady=40)
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Title
        title_label = tk.Label(
            center_frame,
            text="Login to System",
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#34495e'
        )
        title_label.pack(pady=(0, 30))
        
        # Username
        tk.Label(
            center_frame,
            text="Username:",
            font=('Arial', 12),
            fg='white',
            bg='#34495e'
        ).pack(anchor=tk.W)
        
        self.username_entry = tk.Entry(
            center_frame,
            font=('Arial', 12),
            width=25
        )
        self.username_entry.pack(pady=(0, 15))
        self.username_entry.insert(0, "admin")  # Default user
        
        # Password
        tk.Label(
            center_frame,
            text="Password:",
            font=('Arial', 12),
            fg='white',
            bg='#34495e'
        ).pack(anchor=tk.W)
        
        self.password_entry = tk.Entry(
            center_frame,
            font=('Arial', 12),
            width=25,
            show="*"
        )
        self.password_entry.pack(pady=(0, 20))
        self.password_entry.insert(0, "password")  # Default password
        
        # Login button
        login_btn = tk.Button(
            center_frame,
            text="Login",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=10,
            command=self.authenticate_user
        )
        login_btn.pack()
        
        # Error label
        self.login_error = tk.Label(
            center_frame,
            text="",
            font=('Arial', 10),
            fg='#e74c3c',
            bg='#34495e'
        )
        self.login_error.pack(pady=(10, 0))
        
        # Set focus
        self.username_entry.focus()
        self.root.bind('<Return>', lambda e: self.authenticate_user())
        
    def authenticate_user(self):
        """Authenticate user"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Check credentials (in real system, verify against database)
        if username and password:
            # Log login attempt
            self.db.log_event('login_attempt', {
                'username': username,
                'success': True,
                'timestamp': datetime.now().isoformat()
            })
            
            self.current_user = username
            self.logger.info(f"User '{username}' logged in")
            
            # Play login sound
            self.play_sound('login')
            
            # Transition to desktop
            self.root.after(500, self.show_desktop)
        else:
            self.login_error.config(text="Please enter username and password")
            
    def show_desktop(self):
        """Show desktop interface"""
        self.logger.info("Showing desktop")
        
        # Clear login screen
        self.login_frame.destroy()
        
        # Create desktop
        self.desktop = Desktop(self.root, self)
        
    def show_shutdown_screen(self):
        """Display shutdown screen"""
        self.logger.info("Showing shutdown screen")
        
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
        message_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Animate dots
        dots = [".", "..", "..."]
        
        def animate_dots(index=0):
            if index < 10:  # Animate for 5 seconds
                message_label.config(text=f"Shutting down{dots[index % 3]}")
                self.root.after(500, lambda: animate_dots(index + 1))
            else:
                self.root.quit()
        
        # Log shutdown
        self.db.log_event('shutdown', {
            'user': self.current_user,
            'timestamp': datetime.now().isoformat()
        })
        
        # Play shutdown sound
        self.play_sound('shutdown')
        
        animate_dots()
        
    def play_sound(self, sound_type):
        """Play system sounds"""
        try:
            sound_paths = {
                'login': 'assets/sounds/login.wav',
                'logout': 'assets/sounds/logout.wav',
                'shutdown': 'assets/sounds/shutdown.wav',
                'click': 'assets/sounds/click.wav',
                'error': 'assets/sounds/error.wav'
            }
            
            # Create default sounds if they don't exist
            if not os.path.exists('assets'):
                os.makedirs('assets/sounds', exist_ok=True)
                # In a real implementation, you would add actual sound files
                
            # Play sound if file exists
            if sound_type in sound_paths and os.path.exists(sound_paths[sound_type]):
                sound = pygame.mixer.Sound(sound_paths[sound_type])
                sound.play()
        except Exception as e:
            self.logger.error(f"Error playing sound: {e}")
            
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