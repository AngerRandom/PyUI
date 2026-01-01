import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk
import time

class Desktop:
    def __init__(self, root, os_app):
        self.root = root
        self.os_app = os_app
        self.current_theme = 'default'
        
        # Create desktop container
        self.desktop_frame = tk.Frame(root)
        self.desktop_frame.pack(fill=tk.BOTH, expand=True)
        
        # Setup desktop
        self.setup_wallpaper()
        self.setup_taskbar()
        self.setup_icons()
        
    def setup_wallpaper(self):
        """Setup desktop wallpaper"""
        self.wallpaper_label = tk.Label(self.desktop_frame)
        self.wallpaper_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Try to load wallpaper
        try:
            wallpaper_path = 'assets/wallpaper.jpg'
            if os.path.exists(wallpaper_path):
                img = Image.open(wallpaper_path)
                img = img.resize((self.root.winfo_width(), self.root.winfo_height()))
                self.wallpaper_image = ImageTk.PhotoImage(img)
                self.wallpaper_label.config(image=self.wallpaper_image)
            else:
                self.wallpaper_label.config(bg='#2c3e50')
        except Exception as e:
            self.wallpaper_label.config(bg='#2c3e50')
            
    def setup_taskbar(self):
        """Setup taskbar at bottom"""
        self.taskbar = tk.Frame(self.root, bg='#2c3e50', height=40)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Start button
        start_btn = tk.Button(
            self.taskbar,
            text="Start",
            bg='#3498db',
            fg='white',
            padx=20,
            command=self.show_start_menu
        )
        start_btn.pack(side=tk.LEFT, padx=5)
        
        # Taskbar center for running apps
        self.taskbar_center = tk.Frame(self.taskbar, bg='#2c3e50')
        self.taskbar_center.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        # System tray
        self.system_tray = tk.Frame(self.taskbar, bg='#2c3e50')
        self.system_tray.pack(side=tk.RIGHT)
        
        # Time display
        self.time_label = tk.Label(
            self.system_tray,
            font=('Arial', 10),
            bg='#2c3e50',
            fg='white'
        )
        self.time_label.pack(side=tk.RIGHT, padx=10)
        self.update_time()
        
        # Shutdown button
        shutdown_btn = tk.Button(
            self.system_tray,
            text="⏻",
            font=('Arial', 14),
            bg='#e74c3c',
            fg='white',
            command=self.os_app.show_shutdown_screen
        )
        shutdown_btn.pack(side=tk.LEFT, padx=5)
        
    def update_time(self):
        """Update time display"""
        current_time = time.strftime('%H:%M:%S')
        current_date = time.strftime('%Y-%m-%d')
        self.time_label.config(text=f"{current_date} {current_time}")
        self.root.after(1000, self.update_time)
        
    def setup_icons(self):
        """Setup desktop icons"""
        icons_frame = tk.Frame(self.desktop_frame, bg='transparent')
        icons_frame.place(x=20, y=20)
        
        # Define applications
        applications = [
            ("Terminal", "term.png", self.open_terminal),
            ("File Explorer", "files.png", self.open_file_explorer),
            ("Paint", "paint.png", self.open_paint),
            ("Media Player", "media.png", self.open_media_player),
            ("Settings", "settings.png", self.open_settings),
            ("Text Editor", "editor.png", self.open_text_editor)
        ]
        
        for i, (name, icon, command) in enumerate(applications):
            icon_frame = tk.Frame(icons_frame, bg='transparent')
            icon_frame.grid(row=i//4, column=i%4, padx=20, pady=10)
            
            # Icon label
            icon_label = tk.Label(
                icon_frame,
                text="📁",
                font=('Arial', 24),
                bg='transparent',
                fg='white'
            )
            icon_label.pack()
            
            # Icon text
            icon_text = tk.Label(
                icon_frame,
                text=name,
                font=('Arial', 10),
                bg='transparent',
                fg='white'
            )
            icon_text.pack()
            
            # Bind click events
            icon_label.bind('<Button-1>', lambda e, cmd=command: cmd())
            icon_text.bind('<Button-1>', lambda e, cmd=command: cmd())
            
    def show_start_menu(self):
        """Show start menu"""
        if hasattr(self, 'start_menu') and self.start_menu.winfo_exists():
            self.start_menu.destroy()
            return
            
        self.start_menu = tk.Toplevel(self.root)
        self.start_menu.overrideredirect(True)
        self.start_menu.geometry("300x400")
        self.start_menu.configure(bg='#2c3e50')
        
        # Position near start button
        x = self.root.winfo_x() + 50
        y = self.root.winfo_y() + self.root.winfo_height() - 440
        self.start_menu.geometry(f"+{x}+{y}")
        
        # Menu items
        menu_items = [
            ("Terminal", self.open_terminal),
            ("File Explorer", self.open_file_explorer),
            ("Paint", self.open_paint),
            ("Media Player", self.open_media_player),
            ("Settings", self.open_settings),
            ("Calculator", self.open_calculator),
            ("Text Editor", self.open_text_editor),
            ("---", None),
            ("Shutdown", self.os_app.show_shutdown_screen)
        ]
        
        for item, command in menu_items:
            if item == "---":
                ttk.Separator(self.start_menu, orient='horizontal').pack(fill=tk.X, pady=5)
            else:
                btn = tk.Button(
                    self.start_menu,
                    text=item,
                    anchor='w',
                    font=('Arial', 11),
                    bg='#2c3e50',
                    fg='white',
                    padx=20,
                    pady=10,
                    width=20,
                    command=command
                )
                btn.pack()
                
        # Bind close event
        self.start_menu.bind('<FocusOut>', lambda e: self.start_menu.destroy())
        
    def open_terminal(self):
        """Open terminal application"""
        from applications.terminal import TerminalApp
        terminal = TerminalApp(self.root, self.os_app)
        
    def open_file_explorer(self):
        """Open file explorer"""
        from applications.file_explorer import FileExplorer
        explorer = FileExplorer(self.root, self.os_app)
        
    def open_paint(self):
        """Open paint application"""
        from applications.paint import PaintApp
        paint = PaintApp(self.root, self.os_app)
        
    def open_media_player(self):
        """Open media player"""
        from applications.media_player import MediaPlayer
        player = MediaPlayer(self.root, self.os_app)
        
    def open_settings(self):
        """Open settings"""
        from applications.settings import SettingsApp
        settings = SettingsApp(self.root, self.os_app)
        
    def open_text_editor(self):
        """Open text editor"""
        from applications.text_editor import TextEditor
        editor = TextEditor(self.root, self.os_app)
        
    def open_calculator(self):
        """Open calculator"""
        from applications.calculator import Calculator
        calc = Calculator(self.root, self.os_app)