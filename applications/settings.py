# applications/settings.py
import tkinter as tk
from tkinter import filedialog, ttk
import pygame
import os
class SettingsApp:
    def __init__(self, parent, os_app):
        self.os_app = os_app
        self.parent = parent
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Settings")
        self.window.geometry("600x500")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup settings UI"""
        # Notebook for tabs
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Appearance tab
        appearance_frame = tk.Frame(notebook)
        notebook.add(appearance_frame, text="Appearance")
        
        self.setup_appearance_tab(appearance_frame)
        
        # System tab
        system_frame = tk.Frame(notebook)
        notebook.add(system_frame, text="System")
        
        self.setup_system_tab(system_frame)
        
        # Sound tab
        sound_frame = tk.Frame(notebook)
        notebook.add(sound_frame, text="Sound")
        
        self.setup_sound_tab(sound_frame)
        
    def setup_appearance_tab(self, parent):
        """Setup appearance settings"""
        tk.Label(parent, text="Theme:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        themes = ['Default', 'Dark', 'Light', 'Blue', 'Green']
        self.theme_var = tk.StringVar(value='Default')
        
        for theme in themes:
            tk.Radiobutton(
                parent,
                text=theme,
                variable=self.theme_var,
                value=theme
            ).pack(anchor=tk.W, padx=40)
            
        tk.Label(parent, text="Wallpaper:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        wallpaper_frame = tk.Frame(parent)
        wallpaper_frame.pack(fill=tk.X, padx=40, pady=10)
        
        tk.Button(
            wallpaper_frame,
            text="Browse...",
            command=self.change_wallpaper
        ).pack(side=tk.LEFT)
        
        tk.Label(parent, text="Font Size:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        self.font_size = tk.Scale(
            parent,
            from_=8,
            to=24,
            orient=tk.HORIZONTAL,
            length=200
        )
        self.font_size.set(11)
        self.font_size.pack(anchor=tk.W, padx=40)
        
    def setup_system_tab(self, parent):
        """Setup system settings tab with setup options"""
        tk.Label(parent, text="System Information:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        info_frame = tk.Frame(parent)
        info_frame.pack(fill=tk.X, padx=40, pady=10)
        
        # Get system info
        setup_date = self.os_app.db.get_system_info('setup_timestamp', 'Unknown')
        if setup_date != 'Unknown':
            from datetime import datetime
            try:
                dt = datetime.fromtimestamp(float(setup_date))
                setup_date = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                pass
                
        info = [
            ("OS Version:", "Python OS Simulator 2.0"),
            ("Setup Date:", setup_date),
            ("Computer Name:", self.os_app.db.get_system_info('computer_name', 'PythonOS-PC')),
            ("User:", self.os_app.current_user),
            ("Timezone:", self.os_app.db.get_system_info('timezone', 'UTC')),
        ]
        
        for label, value in info:
            frame = tk.Frame(info_frame)
            frame.pack(fill=tk.X, pady=2)
            
            tk.Label(frame, text=label, width=15, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(frame, text=value).pack(side=tk.LEFT)
            
        # Setup options
        tk.Label(parent, text="Setup Options:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, padx=20, pady=(30, 10))
        
        options_frame = tk.Frame(parent, bg='#f8f9fa', relief=tk.SUNKEN, borderwidth=1)
        options_frame.pack(fill=tk.X, padx=40, pady=10)
        
        # Re-run setup button
        rerun_btn = tk.Button(
            options_frame,
            text="Re-run First Time Setup",
            font=('Arial', 11),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=10,
            command=self.rerun_setup
        )
        rerun_btn.pack(pady=10)
        
        tk.Label(
            options_frame,
            text="This will restart the setup wizard and allow you to reconfigure your system.",
            font=('Arial', 9),
            wraplength=400,
            justify=tk.LEFT
        ).pack(pady=(0, 10))
        
    def rerun_setup(self):
        """Re-run the setup wizard"""
        if messagebox.askyesno("Re-run Setup", 
                             "This will restart the setup wizard. Any custom settings may be lost.\nContinue?"):
            # Clear setup completion flag
            self.os_app.db.set_system_info('setup_completed', 'false')
            
            # Restart system to trigger setup
            self.os_app.restart_system()
            
    def setup_sound_tab(self, parent):
        """Setup sound settings"""
        tk.Label(parent, text="Volume Levels:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        settings = [
            ("System Sounds:", 70),
            ("Media Volume:", 80),
            ("Notification:", 60),
            ("Login Sound:", 90)
        ]
        
        for label, default in settings:
            frame = tk.Frame(parent)
            frame.pack(fill=tk.X, padx=40, pady=5)
            
            tk.Label(frame, text=label, width=15).pack(side=tk.LEFT)
            tk.Scale(frame, from_=0, to=100, orient=tk.HORIZONTAL, length=150).pack(side=tk.LEFT)
            
        # Sound effects checkbox
        self.sound_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            parent,
            text="Enable sound effects",
            variable=self.sound_var
        ).pack(anchor=tk.W, padx=40, pady=20)
        
    def change_wallpaper(self):
        """Change desktop wallpaper"""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ('Image files', '*.jpg *.jpeg *.png *.bmp *.gif'),
                ('All files', '*.*')
            ]
        )
        
        if file_path:
            # In a real implementation, you would update the wallpaper
            messagebox.showinfo("Wallpaper", f"Wallpaper set to:\n{file_path}")
