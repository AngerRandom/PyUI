# desktop.py - Complete Desktop class with trash icon
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
            
    def update_time(self):
        """Update time display"""
        current_time = time.strftime('%H:%M:%S')
        current_date = time.strftime('%Y-%m-%d')
        self.time_label.config(text=f"{current_date} {current_time}")
        self.root.after(1000, self.update_time)
        
    def setup_icons(self):
        """Setup desktop icons including trash"""
        icons_frame = tk.Frame(self.desktop_frame, bg='transparent')
        icons_frame.place(x=20, y=20)

        # Add trash icon with indicator
    trash_icon_frame = tk.Frame(icons_frame, bg='transparent')
    trash_icon_frame.grid(row=len(applications)//4, column=len(applications)%4, padx=20, pady=10)
    
    # Get trash count for indicator
    trash_count = self.get_trash_count()
    
    # Icon label with badge
    trash_label = tk.Label(
        trash_icon_frame,
        text="🗑️",
        font=('Arial', 24),
        bg='transparent',
        fg='white'
    )
    trash_label.pack()
    
    # Badge if items in trash
    if trash_count > 0:
        badge = tk.Label(
            trash_icon_frame,
            text=str(trash_count),
            font=('Arial', 8, 'bold'),
            bg='#e74c3c',
            fg='white',
            width=2,
            height=1
        )
        badge.place(relx=0.7, rely=0.1)
        
    # Icon text
    icon_text = tk.Label(
        trash_icon_frame,
        text="Trash Bin",
        font=('Arial', 10),
        bg='transparent',
        fg='white'
    )
    icon_text.pack()
    
    # Bind click events
    trash_label.bind('<Button-1>', lambda e: self.open_trash_bin())
    icon_text.bind('<Button-1>', lambda e: self.open_trash_bin())
    
def get_trash_count(self):
    """Get number of items in trash for current user"""
    try:
        items = self.os_app.db.get_trash_items(self.os_app.current_user)
        return len(items)
    except:
        return 0
        
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
        
        for i, (name, icon, command) in enumerate(applications):
            icon_frame = tk.Frame(icons_frame, bg='transparent')
            icon_frame.grid(row=i//4, column=i%4, padx=20, pady=10)
            
            # Icon label
            if name == "Trash Bin":
                # Get trash count for indicator
                trash_count = self.get_trash_count()
                
                # Icon label with badge
                icon_label = tk.Label(
                    icon_frame,
                    text="🗑️",
                    font=('Arial', 24),
                    bg='transparent',
                    fg='white'
                )
                icon_label.pack()
                
                # Badge if items in trash
                if trash_count > 0:
                    badge = tk.Label(
                        icon_frame,
                        text=str(trash_count),
                        font=('Arial', 8, 'bold'),
                        bg='#e74c3c',
                        fg='white',
                        width=2,
                        height=1
                    )
                    badge.place(relx=0.7, rely=0.1)
            else:
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
            
    def get_trash_count(self):
        """Get number of items in trash for current user"""
        try:
            items = self.os_app.db.get_trash_items(self.os_app.current_user)
            return len(items)
        except:
            return 0
            
    def show_start_menu(self):
        """Show enhanced start menu with trash"""
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
        
        # Menu items - THIS IS WHERE menu_items GOES!
        menu_items = [
            ("Terminal", self.open_terminal),
            ("File Explorer", self.open_file_explorer),
            ("Paint", self.open_paint),
            ("Media Player", self.open_media_player),
            ("Settings", self.open_settings),
            ("Calculator", self.open_calculator),
            ("Text Editor", self.open_text_editor),
            ("Trash Bin", self.open_trash_bin),  # Added trash bin to start menu
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
                    bg=theme['menu_bg'],
                    fg=theme['menu_fg'],
                    padx=20,
                    pady=10,
                    width=20,
                    command=command
                )
                btn.pack()
                
        # Bind close event
        self.start_menu.bind('<FocusOut>', lambda e: self.start_menu.destroy())
        
    # Application launcher methods
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
        
    def open_trash_bin(self):
        """Open trash bin"""
        from applications.trash_bin import TrashBin
        trash = TrashBin(self.root, self.os_app)
        
    def open_browser(self):
        """Open web browser"""
        from applications.browser import Browser
        browser = Browser(self.root, self.os_app)
        
    def open_volume_mixer(self):
        """Open volume mixer"""
        # Implementation would go here
        messagebox.showinfo("Volume Mixer", "Volume mixer would open here")
        
    def open_network_settings(self):
        """Open network settings"""
        # Implementation would go here
        messagebox.showinfo("Network Settings", "Network settings would open here")
