# mobile_desktop.py
import tkinter as tk
from tkinter import ttk, messagebox
import time
import math
from PIL import Image, ImageTk
import os

class MobileDesktop:
    def __init__(self, root, os_app):
        self.root = root
        self.os_app = os_app
        self.current_page = 0
        self.app_pages = []
        self.notifications = []
        
        # Mobile-specific settings
        self.status_bar_height = 30
        self.nav_bar_height = 60
        self.icon_size = 60
        self.icon_padding = 20
        
        # Create mobile interface
        self.setup_mobile_interface()
        
    def setup_mobile_interface(self):
        """Setup mobile interface with status bar, home screen, nav bar"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg='#000000')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status bar (top)
        self.setup_status_bar()
        
        # Home screen (middle)
        self.setup_home_screen()
        
        # Navigation bar (bottom)
        self.setup_navigation_bar()
        
        # Load apps
        self.load_mobile_apps()
        
        # Create app pages
        self.create_app_pages()
        
        # Show first page
        self.show_page(0)
        
        # Start clock update
        self.update_clock()
        
    def setup_status_bar(self):
        """Setup mobile status bar"""
        self.status_bar = tk.Frame(
            self.main_frame,
            bg='#1a1a1a',
            height=self.status_bar_height
        )
        self.status_bar.pack(fill=tk.X, side=tk.TOP)
        self.status_bar.pack_propagate(False)
        
        # Left side: Time
        self.time_label = tk.Label(
            self.status_bar,
            text="12:00",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#1a1a1a'
        )
        self.time_label.pack(side=tk.LEFT, padx=15)
        
        # Center: Date/Status
        self.date_label = tk.Label(
            self.status_bar,
            text="Python OS Mobile",
            font=('Arial', 10),
            fg='#cccccc',
            bg='#1a1a1a'
        )
        self.date_label.pack(side=tk.LEFT, expand=True)
        
        # Right side: Icons
        icon_frame = tk.Frame(self.status_bar, bg='#1a1a1a')
        icon_frame.pack(side=tk.RIGHT, padx=10)
        
        # Signal icon
        self.signal_label = tk.Label(
            icon_frame,
            text="📶",
            font=('Arial', 12),
            fg='white',
            bg='#1a1a1a'
        )
        self.signal_label.pack(side=tk.LEFT, padx=2)
        
        # Wifi icon
        self.wifi_label = tk.Label(
            icon_frame,
            text="📡",
            font=('Arial', 12),
            fg='white',
            bg='#1a1a1a'
        )
        self.wifi_label.pack(side=tk.LEFT, padx=2)
        
        # Battery icon
        self.battery_label = tk.Label(
            icon_frame,
            text="🔋 100%",
            font=('Arial', 12),
            fg='white',
            bg='#1a1a1a'
        )
        self.battery_label.pack(side=tk.LEFT, padx=2)
        
    def setup_home_screen(self):
        """Setup home screen area"""
        self.home_screen = tk.Frame(
            self.main_frame,
            bg='#121212'
        )
        self.home_screen.pack(fill=tk.BOTH, expand=True)
        
        # App container with pages
        self.app_container = tk.Frame(self.home_screen, bg='#121212')
        self.app_container.pack(fill=tk.BOTH, expand=True)
        
        # Page indicators (dots)
        self.page_indicator_frame = tk.Frame(self.home_screen, bg='#121212', height=20)
        self.page_indicator_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.page_indicators = []
        
    def setup_navigation_bar(self):
        """Setup bottom navigation bar"""
        self.nav_bar = tk.Frame(
            self.main_frame,
            bg='#1a1a1a',
            height=self.nav_bar_height
        )
        self.nav_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.nav_bar.pack_propagate(False)
        
        # Navigation buttons
        nav_buttons = [
            ("📞", "Phone", self.open_phone),
            ("📱", "Apps", self.show_app_drawer),
            ("🏠", "Home", lambda: self.show_page(0)),
            ("✉️", "Messages", self.open_messages),
            ("👤", "Contacts", self.open_contacts)
        ]
        
        for icon, text, command in nav_buttons:
            btn_frame = tk.Frame(self.nav_bar, bg='#1a1a1a')
            btn_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
            
            btn = tk.Label(
                btn_frame,
                text=icon,
                font=('Arial', 20),
                fg='white',
                bg='#1a1a1a',
                cursor='hand2'
            )
            btn.pack(pady=(5, 0))
            btn.bind('<Button-1>', lambda e, cmd=command: cmd())
            
            label = tk.Label(
                btn_frame,
                text=text,
                font=('Arial', 8),
                fg='#cccccc',
                bg='#1a1a1a'
            )
            label.pack()
            
    def load_mobile_apps(self):
        """Load mobile-optimized apps"""
        self.mobile_apps = [
            # Core apps
            ("Phone", "📞", self.open_phone, "#4CAF50"),
            ("Messages", "✉️", self.open_messages, "#2196F3"),
            ("Contacts", "👥", self.open_contacts, "#9C27B0"),
            ("Camera", "📷", self.open_camera, "#FF9800"),
            ("Gallery", "🖼️", self.open_gallery, "#E91E63"),
            
            # Utility apps
            ("Calculator", "🧮", self.open_calculator, "#795548"),
            ("Calendar", "📅", self.open_calendar, "#009688"),
            ("Clock", "⏰", self.open_clock, "#3F51B5"),
            ("Weather", "☀️", self.open_weather, "#FFC107"),
            ("Notes", "📝", self.open_notes, "#8BC34A"),
            
            # System apps
            ("Settings", "⚙️", self.open_settings, "#607D8B"),
            ("File Manager", "📁", self.open_file_manager, "#673AB7"),
            ("Browser", "🌐", self.open_browser, "#00BCD4"),
            ("Music", "🎵", self.open_music, "#F44336"),
            ("Maps", "🗺️", self.open_maps, "#4CAF50"),
            
            # More apps
            ("Email", "📧", self.open_email, "#FF5722"),
            ("Store", "🛒", self.open_store, "#9C27B0"),
            ("Health", "❤️", self.open_health, "#E91E63"),
            ("Wallet", "💰", self.open_wallet, "#FF9800"),
            ("Games", "🎮", self.open_games, "#2196F3")
        ]
        
    def create_app_pages(self):
        """Create pages for apps (4x4 grid per page)"""
        apps_per_page = 12  # 4x3 grid
        num_pages = math.ceil(len(self.mobile_apps) / apps_per_page)
        
        # Clear existing pages
        for widget in self.app_container.winfo_children():
            widget.destroy()
            
        self.app_pages = []
        self.page_indicators = []
        
        # Clear page indicators
        for widget in self.page_indicator_frame.winfo_children():
            widget.destroy()
            
        # Create pages
        for page_num in range(num_pages):
            # Create page frame
            page_frame = tk.Frame(self.app_container, bg='#121212')
            self.app_pages.append(page_frame)
            
            # Create page indicator
            indicator = tk.Label(
                self.page_indicator_frame,
                text="●",
                font=('Arial', 12),
                fg='#666666' if page_num != 0 else '#ffffff',
                bg='#121212',
                cursor='hand2'
            )
            indicator.pack(side=tk.LEFT, padx=2)
            indicator.bind('<Button-1>', lambda e, p=page_num: self.show_page(p))
            self.page_indicators.append(indicator)
            
            # Calculate grid
            rows = 4
            cols = 3
            
            # Add apps to this page
            start_idx = page_num * apps_per_page
            end_idx = min(start_idx + apps_per_page, len(self.mobile_apps))
            
            for idx in range(start_idx, end_idx):
                app_name, app_icon, app_command, app_color = self.mobile_apps[idx]
                app_index = idx - start_idx
                
                row = app_index // cols
                col = app_index % cols
                
                # Create app button
                self.create_app_button(page_frame, app_name, app_icon, app_command, 
                                     app_color, row, col)
                                     
    def create_app_button(self, parent, name, icon, command, color, row, col):
        """Create a mobile app button"""
        button_frame = tk.Frame(
            parent,
            bg='#121212',
            width=self.icon_size + self.icon_padding * 2,
            height=self.icon_size + self.icon_padding * 2 + 30
        )
        button_frame.grid(row=row, column=col, padx=5, pady=5)
        button_frame.grid_propagate(False)
        
        # Icon background
        icon_bg = tk.Frame(
            button_frame,
            bg=color,
            width=self.icon_size,
            height=self.icon_size,
            relief=tk.FLAT
        )
        icon_bg.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        
        # Icon
        icon_label = tk.Label(
            icon_bg,
            text=icon,
            font=('Arial', 24),
            bg=color,
            fg='white'
        )
        icon_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # App name
        name_label = tk.Label(
            button_frame,
            text=name,
            font=('Arial', 9),
            fg='white',
            bg='#121212',
            wraplength=80
        )
        name_label.place(relx=0.5, rely=0.85, anchor=tk.CENTER)
        
        # Bind click event
        icon_bg.bind('<Button-1>', lambda e: command())
        icon_label.bind('<Button-1>', lambda e: command())
        name_label.bind('<Button-1>', lambda e: command())
        
    def show_page(self, page_num):
        """Show specific app page"""
        self.current_page = page_num
        
        # Hide all pages
        for page in self.app_pages:
            page.place_forget()
            
        # Show selected page
        self.app_pages[page_num].place(relx=0.5, rely=0.5, anchor=tk.CENTER, 
                                      relwidth=1.0, relheight=1.0)
        
        # Update page indicators
        for i, indicator in enumerate(self.page_indicators):
            indicator.config(fg='#ffffff' if i == page_num else '#666666')
            
    def update_clock(self):
        """Update clock in status bar"""
        current_time = time.strftime('%H:%M')
        current_date = time.strftime('%b %d')
        
        self.time_label.config(text=current_time)
        self.date_label.config(text=current_date)
        
        # Update every minute
        self.root.after(60000, self.update_clock)
        
    def show_app_drawer(self):
        """Show app drawer (all apps)"""
        AppDrawer(self.root, self.os_app, self.mobile_apps)
        
    # App launcher methods
    def open_phone(self):
        """Open phone app"""
        from applications.mobile_phone import MobilePhone
        MobilePhone(self.root, self.os_app)
        
    def open_messages(self):
        """Open messages app"""
        from applications.mobile_messages import MobileMessages
        MobileMessages(self.root, self.os_app)
        
    def open_contacts(self):
        """Open contacts app"""
        from applications.mobile_contacts import MobileContacts
        MobileContacts(self.root, self.os_app)
        
    def open_camera(self):
        """Open camera app"""
        from applications.mobile_camera import MobileCamera
        MobileCamera(self.root, self.os_app)
        
    def open_gallery(self):
        """Open gallery app"""
        from applications.mobile_gallery import MobileGallery
        MobileGallery(self.root, self.os_app)
        
    def open_calculator(self):
        """Open calculator app"""
        from applications.mobile_calculator import MobileCalculator
        MobileCalculator(self.root, self.os_app)
        
    def open_calendar(self):
        """Open calendar app"""
        from applications.mobile_calendar import MobileCalendar
        MobileCalendar(self.root, self.os_app)
        
    def open_clock(self):
        """Open clock app"""
        from applications.mobile_clock import MobileClock
        MobileClock(self.root, self.os_app)
        
    def open_weather(self):
        """Open weather app"""
        from applications.mobile_weather import MobileWeather
        MobileWeather(self.root, self.os_app)
        
    def open_notes(self):
        """Open notes app"""
        from applications.mobile_notes import MobileNotes
        MobileNotes(self.root, self.os_app)
        
    def open_settings(self):
        """Open mobile settings"""
        from applications.mobile_settings import MobileSettings
        MobileSettings(self.root, self.os_app)
        
    def open_file_manager(self):
        """Open mobile file manager"""
        from applications.mobile_file_manager import MobileFileManager
        MobileFileManager(self.root, self.os_app)
        
    def open_browser(self):
        """Open mobile browser"""
        from applications.mobile_browser import MobileBrowser
        MobileBrowser(self.root, self.os_app)
        
    def open_music(self):
        """Open music player"""
        from applications.mobile_music import MobileMusic
        MobileMusic(self.root, self.os_app)
        
    def open_maps(self):
        """Open maps app"""
        from applications.mobile_maps import MobileMaps
        MobileMaps(self.root, self.os_app)
        
    def open_email(self):
        """Open email app"""
        from applications.mobile_email import MobileEmail
        MobileEmail(self.root, self.os_app)
        
    def open_store(self):
        """Open app store"""
        from applications.mobile_store import MobileStore
        MobileStore(self.root, self.os_app)
        
    def open_health(self):
        """Open health app"""
        from applications.mobile_health import MobileHealth
        MobileHealth(self.root, self.os_app)
        
    def open_wallet(self):
        """Open wallet app"""
        from applications.mobile_wallet import MobileWallet
        MobileWallet(self.root, self.os_app)
        
    def open_games(self):
        """Open games"""
        from applications.mobile_games import MobileGames
        MobileGames(self.root, self.os_app)
        
    def show_notification(self, title, message, app_icon="📱"):
        """Show mobile notification"""
        # Create notification
        notification = {
            'title': title,
            'message': message,
            'icon': app_icon,
            'time': time.strftime('%H:%M')
        }
        self.notifications.append(notification)
        
        # Show notification banner (simplified)
        print(f"Notification: {title} - {message}")