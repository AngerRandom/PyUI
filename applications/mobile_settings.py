# applications/mobile_settings.py
import tkinter as tk
from tkinter import ttk, messagebox

class MobileSettings:
    def __init__(self, parent, os_app):
        self.os_app = os_app
        self.parent = parent
        
        # Create settings window
        self.window = tk.Toplevel(parent)
        self.window.title("Settings")
        self.window.geometry("360x600")
        
        self.setup_settings()
        
    def setup_settings(self):
        """Setup mobile settings interface"""
        # Header
        header_frame = tk.Frame(self.window, bg='#607D8B', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="Settings",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#607D8B'
        ).pack(pady=15)
        
        # Settings list (scrollable)
        self.setup_settings_list()
        
    def setup_settings_list(self):
        """Setup scrollable settings list"""
        # Container
        canvas = tk.Canvas(self.window, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Settings categories
        categories = [
            ("Network & Internet", "📶", [
                ("Wi-Fi", self.open_wifi),
                ("Mobile network", self.open_mobile_network),
                ("Hotspot & tethering", self.open_hotspot),
                ("VPN", self.open_vpn)
            ]),
            ("Connected devices", "🔗", [
                ("Bluetooth", self.open_bluetooth),
                ("NFC", self.open_nfc),
                ("USB", self.open_usb)
            ]),
            ("Apps & notifications", "📱", [
                ("App permissions", self.open_app_permissions),
                ("Default apps", self.open_default_apps),
                ("Notifications", self.open_notifications)
            ]),
            ("Battery", "🔋", [
                ("Battery saver", self.open_battery_saver),
                ("Battery usage", self.open_battery_usage)
            ]),
            ("Display", "🖥️", [
                ("Wallpaper", self.open_wallpaper),
                ("Theme", self.open_theme),
                ("Font size", self.open_font_size),
                ("Brightness", self.open_brightness)
            ]),
            ("Sound", "🔊", [
                ("Volume", self.open_volume),
                ("Ringtone", self.open_ringtone),
                ("Vibration", self.open_vibration)
            ]),
            ("Storage", "💾", [
                ("Storage usage", self.open_storage),
                ("Smart storage", self.open_smart_storage)
            ]),
            ("Security", "🔒", [
                ("Screen lock", self.open_screen_lock),
                ("Fingerprint", self.open_fingerprint),
                ("Encryption", self.open_encryption)
            ]),
            ("Accounts", "👤", [
                ("Add account", self.open_add_account),
                ("Sync", self.open_sync)
            ]),
            ("System", "⚙️", [
                ("About phone", self.open_about),
                ("System updates", self.open_updates),
                ("Reset options", self.open_reset)
            ])
        ]
        
        # Create category sections
        for category_name, icon, items in categories:
            self.create_category(scrollable_frame, category_name, icon, items)
            
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_category(self, parent, name, icon, items):
        """Create a settings category"""
        # Category header
        header_frame = tk.Frame(parent, bg='#f5f5f5', height=40)
        header_frame.pack(fill=tk.X, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text=f"{icon} {name}",
            font=('Arial', 12, 'bold'),
            fg='#333333',
            bg='#f5f5f5'
        ).pack(side=tk.LEFT, padx=15, pady=10)
        
        # Settings items
        for item_name, item_command in items:
            item_frame = tk.Frame(parent, bg='white', height=50)
            item_frame.pack(fill=tk.X, pady=1)
            item_frame.pack_propagate(False)
            
            # Item label
            tk.Label(
                item_frame,
                text=item_name,
                font=('Arial', 14),
                bg='white',
                fg='#333333',
                anchor=tk.W
            ).pack(side=tk.LEFT, padx=20, pady=15)
            
            # Arrow
            tk.Label(
                item_frame,
                text="›",
                font=('Arial', 20),
                bg='white',
                fg='#cccccc'
            ).pack(side=tk.RIGHT, padx=20)
            
            # Bind click
            item_frame.bind('<Button-1>', lambda e, cmd=item_command: cmd())
            
    # Settings category handlers
    def open_wifi(self):
        self.show_setting_detail("Wi-Fi", "Configure wireless networks")
        
    def open_mobile_network(self):
        self.show_setting_detail("Mobile Network", "Configure cellular data and network")
        
    def open_hotspot(self):
        self.show_setting_detail("Hotspot", "Set up mobile hotspot")
        
    def open_vpn(self):
        self.show_setting_detail("VPN", "Configure virtual private network")
        
    def open_bluetooth(self):
        self.show_setting_detail("Bluetooth", "Pair and manage Bluetooth devices")
        
    def open_nfc(self):
        self.show_setting_detail("NFC", "Near field communication settings")
        
    def open_usb(self):
        self.show_setting_detail("USB", "USB connection preferences")
        
    def open_app_permissions(self):
        self.show_setting_detail("App Permissions", "Manage app permissions")
        
    def open_default_apps(self):
        self.show_setting_detail("Default Apps", "Set default applications")
        
    def open_notifications(self):
        self.show_setting_detail("Notifications", "Configure notification settings")
        
    def open_battery_saver(self):
        self.show_setting_detail("Battery Saver", "Extend battery life")
        
    def open_battery_usage(self):
        self.show_setting_detail("Battery Usage", "View battery consumption")
        
    def open_wallpaper(self):
        self.show_setting_detail("Wallpaper", "Change home screen wallpaper")
        
    def open_theme(self):
        self.show_setting_detail("Theme", "Change system theme")
        
    def open_font_size(self):
        self.show_setting_detail("Font Size", "Adjust text size")
        
    def open_brightness(self):
        self.show_setting_detail("Brightness", "Adjust screen brightness")
        
    def open_volume(self):
        self.show_setting_detail("Volume", "Adjust sound volumes")
        
    def open_ringtone(self):
        self.show_setting_detail("Ringtone", "Change ringtone")
        
    def open_vibration(self):
        self.show_setting_detail("Vibration", "Configure vibration settings")
        
    def open_storage(self):
        self.show_setting_detail("Storage", "View storage usage")
        
    def open_smart_storage(self):
        self.show_setting_detail("Smart Storage", "Automatic storage management")
        
    def open_screen_lock(self):
        self.show_setting_detail("Screen Lock", "Set up screen lock security")
        
    def open_fingerprint(self):
        self.show_setting_detail("Fingerprint", "Configure fingerprint unlock")
        
    def open_encryption(self):
        self.show_setting_detail("Encryption", "Device encryption settings")
        
    def open_add_account(self):
        self.show_setting_detail("Add Account", "Add email or other accounts")
        
    def open_sync(self):
        self.show_setting_detail("Sync", "Configure account synchronization")
        
    def open_about(self):
        self.show_about_phone()
        
    def open_updates(self):
        self.show_setting_detail("Updates", "Check for system updates")
        
    def open_reset(self):
        self.show_reset_options()
        
    def show_setting_detail(self, title, description):
        """Show setting detail page"""
        detail_window = tk.Toplevel(self.window)
        detail_window.title(title)
        detail_window.geometry("360x500")
        
        # Header
        header = tk.Frame(detail_window, bg='#607D8B', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=title,
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#607D8B'
        ).pack(pady=15)
        
        # Back button
        back_btn = tk.Label(
            header,
            text="‹",
            font=('Arial', 30),
            fg='white',
            bg='#607D8B',
            cursor='hand2'
        )
        back_btn.pack(side=tk.LEFT, padx=10)
        back_btn.bind('<Button-1>', lambda e: detail_window.destroy())
        
        # Content
        content = tk.Frame(detail_window, bg='white')
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            content,
            text=description,
            font=('Arial', 14),
            fg='#666666',
            bg='white'
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # Simulated setting controls
        if title == "Wi-Fi":
            self.create_wifi_controls(content)
        elif title == "Brightness":
            self.create_brightness_controls(content)
        elif title == "Theme":
            self.create_theme_controls(content)
            
    def create_wifi_controls(self, parent):
        """Create WiFi controls"""
        # WiFi toggle
        toggle_frame = tk.Frame(parent, bg='white')
        toggle_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            toggle_frame,
            text="Wi-Fi",
            font=('Arial', 16),
            bg='white',
            fg='#333333'
        ).pack(side=tk.LEFT)
        
        wifi_var = tk.BooleanVar(value=True)
        wifi_toggle = tk.Checkbutton(
            toggle_frame,
            variable=wifi_var,
            bg='white'
        )
        wifi_toggle.pack(side=tk.RIGHT)
        
        # Available networks
        networks_frame = tk.Frame(parent, bg='white')
        networks_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        tk.Label(
            networks_frame,
            text="Available Networks:",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#333333'
        ).pack(anchor=tk.W, pady=(0, 10))
        
        networks = [
            ("HomeWiFi", "🔒", "Excellent"),
            ("GuestNetwork", "", "Good"),
            ("AndroidAP", "🔒", "Fair"),
            ("FreePublicWiFi", "", "Weak")
        ]
        
        for name, security, strength in networks:
            net_frame = tk.Frame(networks_frame, bg='#f5f5f5', height=50)
            net_frame.pack(fill=tk.X, pady=2)
            net_frame.pack_propagate(False)
            
            tk.Label(
                net_frame,
                text=name,
                font=('Arial', 14),
                bg='#f5f5f5',
                fg='#333333'
            ).pack(side=tk.LEFT, padx=15, pady=15)
            
            tk.Label(
                net_frame,
                text=security,
                font=('Arial', 14),
                bg='#f5f5f5',
                fg='#666666'
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Label(
                net_frame,
                text=strength,
                font=('Arial', 12),
                bg='#f5f5f5',
                fg='#666666'
            ).pack(side=tk.RIGHT, padx=15)
            
    def create_brightness_controls(self, parent):
        """Create brightness controls"""
        tk.Label(
            parent,
            text="Adjust Screen Brightness",
            font=('Arial', 16),
            bg='white',
            fg='#333333'
        ).pack(anchor=tk.W, pady=(0, 20))
        
        brightness_var = tk.IntVar(value=70)
        
        scale = tk.Scale(
            parent,
            from_=0,
            to=100,
            variable=brightness_var,
            orient=tk.HORIZONTAL,
            length=300,
            bg='white',
            fg='#333333'
        )
        scale.pack(pady=20)
        
        # Auto-brightness
        auto_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            parent,
            text="Adaptive brightness",
            variable=auto_var,
            font=('Arial', 14),
            bg='white',
            fg='#333333'
        ).pack(anchor=tk.W, pady=20)
        
    def create_theme_controls(self, parent):
        """Create theme controls"""
        themes = [
            ("Light", "Light theme with white background"),
            ("Dark", "Dark theme for better battery life"),
            ("Auto", "Switch based on time of day"),
            ("Blue", "Blue accent theme"),
            ("Green", "Green accent theme")
        ]
        
        theme_var = tk.StringVar(value="Dark")
        
        for theme_name, theme_desc in themes:
            theme_frame = tk.Frame(parent, bg='white', height=60)
            theme_frame.pack(fill=tk.X, pady=5)
            theme_frame.pack_propagate(False)
            
            rb = tk.Radiobutton(
                theme_frame,
                text=theme_name,
                variable=theme_var,
                value=theme_name,
                font=('Arial', 14),
                bg='white',
                fg='#333333'
            )
            rb.pack(side=tk.LEFT, padx=10, pady=15)
            
            tk.Label(
                theme_frame,
                text=theme_desc,
                font=('Arial', 11),
                bg='white',
                fg='#666666'
            ).pack(side=tk.LEFT, padx=10, pady=15)
            
    def show_about_phone(self):
        """Show about phone information"""
        about_window = tk.Toplevel(self.window)
        about_window.title("About Phone")
        about_window.geometry("360x500")
        
        # Header
        header = tk.Frame(about_window, bg='#607D8B', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="About Phone",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#607D8B'
        ).pack(pady=15)
        
        # Back button
        back_btn = tk.Label(
            header,
            text="‹",
            font=('Arial', 30),
            fg='white',
            bg='#607D8B',
            cursor='hand2'
        )
        back_btn.pack(side=tk.LEFT, padx=10)
        back_btn.bind('<Button-1>', lambda e: about_window.destroy())
        
        # Content
        content = tk.Frame(about_window, bg='white')
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Device info
        info = [
            ("Device name:", f"PythonOS Mobile"),
            ("Model:", "PYOS-Mobile-Simulator"),
            ("Android version:", "Python OS 2.0"),
            ("Kernel version:", "3.18.71-python-sim"),
            ("Build number:", "PYOSM.2024.01.001"),
            ("Serial number:", "PYOS-2024-0001"),
            ("IMEI:", "Simulated-IMEI-123456"),
            ("SIM status:", "Active"),
            ("Network:", "Python Mobile Network"),
            ("Signal strength:", "Excellent"),
            ("Battery health:", "Good (100%)"),
            ("Storage:", "64GB (45GB available)"),
            ("RAM:", "4GB"),
            ("Processor:", "Python Virtual CPU"),
            ("Security patch:", "January 1, 2024")
        ]
        
        for label, value in info:
            frame = tk.Frame(content, bg='white')
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                frame,
                text=label,
                font=('Arial', 12, 'bold'),
                bg='white',
                fg='#333333',
                width=15,
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            tk.Label(
                frame,
                text=value,
                font=('Arial', 12),
                bg='white',
                fg='#666666',
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
        # Legal info
        legal_frame = tk.Frame(content, bg='white')
        legal_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(
            legal_frame,
            text="Legal Information",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#333333'
        ).pack(anchor=tk.W, pady=(0, 10))
        
        legal_text = """Python OS Mobile Simulator
Version 2.0
© 2024 Python OS Project

This is a simulation for educational purposes.
Not a real mobile operating system.
"""
        
        tk.Label(
            legal_frame,
            text=legal_text,
            font=('Arial', 10),
            bg='white',
            fg='#666666',
            justify=tk.LEFT
        ).pack(anchor=tk.W)
        
    def show_reset_options(self):
        """Show reset options"""
        reset_window = tk.Toplevel(self.window)
        reset_window.title("Reset Options")
        reset_window.geometry("360x500")
        
        # Header
        header = tk.Frame(reset_window, bg='#607D8B', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="Reset Options",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#607D8B'
        ).pack(pady=15)
        
        # Back button
        back_btn = tk.Label(
            header,
            text="‹",
            font=('Arial', 30),
            fg='white',
            bg='#607D8B',
            cursor='hand2'
        )
        back_btn.pack(side=tk.LEFT, padx=10)
        back_btn.bind('<Button-1>', lambda e: reset_window.destroy())
        
        # Warning
        warning_frame = tk.Frame(reset_window, bg='#fff3cd')
        warning_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            warning_frame,
            text="⚠️ Warning",
            font=('Arial', 14, 'bold'),
            bg='#fff3cd',
            fg='#856404'
        ).pack(pady=10)
        
        tk.Label(
            warning_frame,
            text="Resetting will erase data from your device.",
            font=('Arial', 12),
            bg='#fff3cd',
            fg='#856404',
            wraplength=300
        ).pack(pady=(0, 10), padx=10)
        
        # Reset options
        options_frame = tk.Frame(reset_window, bg='white')
        options_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        reset_options = [
            ("Reset app preferences", "Resets app permissions and defaults"),
            ("Reset network settings", "Resets Wi-Fi, mobile & Bluetooth"),
            ("Reset accessibility", "Resets accessibility settings"),
            ("Erase all data (factory reset)", "Completely erases all data")
        ]
        
        for option_name, option_desc in reset_options:
            option_frame = tk.Frame(options_frame, bg='white', height=60)
            option_frame.pack(fill=tk.X, pady=5)
            option_frame.pack_propagate(False)
            
            tk.Label(
                option_frame,
                text=option_name,
                font=('Arial', 14),
                bg='white',
                fg='#333333'
            ).pack(anchor=tk.W, padx=10, pady=5)
            
            tk.Label(
                option_frame,
                text=option_desc,
                font=('Arial', 11),
                bg='white',
                fg='#666666'
            ).pack(anchor=tk.W, padx=10, pady=(0, 5))
            
            # Reset button
            reset_btn = tk.Button(
                option_frame,
                text="Reset",
                font=('Arial', 12),
                bg='#dc3545',
                fg='white',
                command=lambda o=option_name: self.confirm_reset(o)
            )
            reset_btn.pack(side=tk.RIGHT, padx=10)
            
    def confirm_reset(self, option):
        """Confirm reset action"""
        confirm = messagebox.askyesno(
            "Confirm Reset",
            f"Are you sure you want to:\n{option}?\n\n"
            "This action cannot be undone."
        )
        
        if confirm:
            messagebox.showinfo(
                "Reset Initiated",
                f"{option} has been initiated.\n"
                "The device will restart to complete the process."
            )
            
            # Log the reset
            self.os_app.db.log_event('mobile_reset', {
                'option': option,
                'user': self.os_app.current_user,
                'time': time.time()
            })