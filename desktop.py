# desktop.py - Enhanced with window management
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
        
        # Window management
        self.taskbar_buttons = {}
        
        # Start menu
        self.start_menu = None
        
    def setup_wallpaper(self):
        """Setup desktop wallpaper with theme support"""
        self.wallpaper_label = tk.Label(self.desktop_frame)
        self.wallpaper_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Try to load wallpaper from theme
        theme = self.os_app.theme_manager.get_current_theme()
        wallpaper_path = theme.get('wallpaper', 'assets/wallpaper.jpg')
        
        try:
            if os.path.exists(wallpaper_path):
                img = Image.open(wallpaper_path)
                img = img.resize((self.root.winfo_width(), self.root.winfo_height()))
                self.wallpaper_image = ImageTk.PhotoImage(img)
                self.wallpaper_label.config(image=self.wallpaper_image)
            else:
                self.wallpaper_label.config(bg=theme['background'])
        except Exception as e:
            self.wallpaper_label.config(bg=theme['background'])
            
    def setup_taskbar(self):
        """Setup taskbar with window management"""
        theme = self.os_app.theme_manager.get_current_theme()
        
        self.taskbar = tk.Frame(self.root, bg=theme['taskbar_bg'], height=40)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Start button and menu
        start_btn = tk.Button(
            self.taskbar,
            text="Start",
            bg=theme['start_button_bg'],
            fg=theme['start_button_fg'],
            padx=20,
            cursor='hand2',
            command=self.show_start_menu
        )
        start_btn.pack(side=tk.LEFT, padx=5)
        
        # Taskbar center for running apps
        self.taskbar_center = tk.Frame(self.taskbar, bg=theme['taskbar_bg'])
        self.taskbar_center.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        # Quick launch icons
        quick_launch_frame = tk.Frame(self.taskbar, bg=theme['taskbar_bg'])
        quick_launch_frame.pack(side=tk.LEFT, padx=5)
        
        quick_apps = [
            ('🌐', self.open_browser),
            ('📁', self.open_file_explorer),
            ('🎵', self.open_media_player),
            ('🖌️', self.open_paint)
        ]
        
        for icon, command in quick_apps:
            btn = tk.Button(
                quick_launch_frame,
                text=icon,
                font=('Arial', 14),
                bg=theme['taskbar_bg'],
                fg=theme['taskbar_fg'],
                borderwidth=0,
                cursor='hand2',
                command=command
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # System tray
        self.system_tray = tk.Frame(self.taskbar, bg=theme['taskbar_bg'])
        self.system_tray.pack(side=tk.RIGHT)
        
        # Time display
        time_frame = tk.Frame(self.system_tray, bg=theme['taskbar_bg'])
        time_frame.pack(side=tk.RIGHT, padx=10)
        
        self.time_label = tk.Label(
            time_frame,
            font=('Arial', 10),
            bg=theme['taskbar_bg'],
            fg=theme['taskbar_fg']
        )
        self.time_label.pack()
        self.update_time()
        
        # System tray icons
        tray_icons = [
            ('🔊', self.open_volume_mixer),
            ('📶', self.open_network_settings),
            ('⚙️', self.open_settings),
            ('⏻', self.os_app.show_shutdown_screen, theme['error']),
            ('↻', self.os_app.restart_system, theme['warning'])
        ]
        
        for icon, command, *color in tray_icons:
            bg_color = color[0] if color else theme['taskbar_bg']
            btn = tk.Button(
                self.system_tray,
                text=icon,
                font=('Arial', 12),
                bg=bg_color,
                fg='white',
                borderwidth=0,
                cursor='hand2',
                command=command
            )
            btn.pack(side=tk.LEFT, padx=2)

    def setup_icons(self):
        """Setup desktop icons including trash"""
        icons_frame = tk.Frame(self.desktop_frame, bg='transparent')
        icons_frame.place(x=20, y=20)
        
        # Define applications including trash
        applications = [
            ("Terminal", "term.png", self.open_terminal),
            ("File Explorer", "files.png", self.open_file_explorer),
            ("Paint", "paint.png", self.open_paint),
            ("Media Player", "media.png", self.open_media_player),
            ("Settings", "settings.png", self.open_settings),
            ("Text Editor", "editor.png", self.open_text_editor),
            ("Trash Bin", "trash.png", self.open_trash_bin)  # Added trash
        ]
            
    def update_time(self):
        """Update time display"""
        current_time = time.strftime('%H:%M:%S')
        current_date = time.strftime('%Y-%m-%d')
        self.time_label.config(text=f"{current_date} {current_time}")
        self.root.after(1000, self.update_time)
        
    def show_start_menu(self):
        """Show enhanced start menu"""
        if self.start_menu and self.start_menu.winfo_exists():
            self.start_menu.destroy()
            self.start_menu = None
            return
            
        theme = self.os_app.theme_manager.get_current_theme()
        
        self.start_menu = tk.Toplevel(self.root)
        self.start_menu.overrideredirect(True)
        self.start_menu.geometry("350x500")
        self.start_menu.configure(bg=theme['menu_bg'])
        
        # Position near start button
        x = self.root.winfo_x() + 50
        y = self.root.winfo_y() + self.root.winfo_height() - 540
        self.start_menu.geometry(f"+{x}+{y}")
        
        # User info section
        user_frame = tk.Frame(self.start_menu, bg=theme['accent'], height=80)
        user_frame.pack(fill=tk.X)
        
        tk.Label(
            user_frame,
            text=self.os_app.current_user,
            font=('Arial', 16, 'bold'),
            fg='white',
            bg=theme['accent']
        ).pack(side=tk.LEFT, padx=20, pady=20)
        
        # Application list
        menu_items = [
            ("Terminal", self.open_terminal),
            ("File Explorer", self.open_file_explorer),
            ("Paint", self.open_paint),
            ("Media Player", self.open_media_player),
            ("Settings", self.open_settings),
            ("Calculator", self.open_calculator),
            ("Text Editor", self.open_text_editor),
            ("Trash Bin", self.open_trash_bin),  # Added
            ("---", None),
            ("Shutdown", self.os_app.show_shutdown_screen)
        ]
        app_list_frame = tk.Frame(self.start_menu, bg=theme['menu_bg'])
        app_list_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Create scrollable app list
        canvas = tk.Canvas(app_list_frame, bg=theme['menu_bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(app_list_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=theme['menu_bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Group apps by category
        apps_by_category = {}
        for app_name, app_info in self.os_app.installed_apps.items():
            # Get category from database
            category = "Applications"
            apps_by_category.setdefault(category, []).append((app_name, app_info))
        
        # Display apps
        for category, apps in apps_by_category.items():
            tk.Label(
                scrollable_frame,
                text=category,
                font=('Arial', 10, 'bold'),
                fg=theme['menu_fg'],
                bg=theme['menu_bg'],
                anchor=tk.W
            ).pack(fill=tk.X, padx=10, pady=(10, 5))
            
            for app_name, app_info in apps:
                btn = tk.Button(
                    scrollable_frame,
                    text=f"  {app_name}",
                    font=('Arial', 11),
                    bg=theme['menu_bg'],
                    fg=theme['menu_fg'],
                    anchor=tk.W,
                    padx=10,
                    pady=8,
                    cursor='hand2',
                    command=lambda name=app_name: self.launch_app_from_menu(name)
                )
                btn.pack(fill=tk.X, padx=5)
                
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bottom section
        bottom_frame = tk.Frame(self.start_menu, bg=theme['menu_bg'], height=40)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        bottom_buttons = [
            ("Settings", self.open_settings),
            ("File Explorer", self.open_file_explorer),
            ("Terminal", self.open_terminal)
        ]
        
        for text, command in bottom_buttons:
            tk.Button(
                bottom_frame,
                text=text,
                font=('Arial', 9),
                bg=theme['menu_bg'],
                fg=theme['menu_fg'],
                borderwidth=0,
                cursor='hand2',
                command=command
            ).pack(side=tk.LEFT, padx=10)
        
        # Bind close event
        self.start_menu.bind('<FocusOut>', lambda e: self.start_menu.destroy())
        
    def launch_app_from_menu(self, app_name):
        """Launch application from start menu"""
        self.os_app.launch_application(app_name)
        if self.start_menu:
            self.start_menu.destroy()
            self.start_menu = None

    def open_trash_bin(self):
        """Open trash bin"""
        from applications.trash_bin import TrashBin
        trash = TrashBin(self.root, self.os_app)
