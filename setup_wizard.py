# setup_wizard.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import time

class FirstTimeSetup:
    def __init__(self, root, os_app):
        self.root = root
        self.os_app = os_app
        self.current_step = 0
        self.setup_data = {
            'user_name': '',
            'user_password': '',
            'computer_name': 'PythonOS-PC',
            'timezone': 'UTC',
            'theme': 'default',
            'wallpaper': None,
            'install_apps': True,
            'updates': True,
            'privacy': {},
            'completed': False
        }
        
        # Create setup window
        self.window = tk.Toplevel(root)
        self.window.title("Python OS Setup")
        self.window.geometry("800x600")
        self.window.configure(bg='#2c3e50')
        
        # Make it modal
        self.window.transient(root)
        self.window.grab_set()
        self.window.focus_force()
        
        # Center window
        self.center_window()
        
        # Setup steps
        self.steps = [
            self.step_welcome,
            self.step_license,
            self.step_user_account,
            self.step_computer_name,
            self.step_timezone,
            self.step_theme,
            self.step_privacy,
            self.step_install_apps,
            self.step_final
        ]
        
        # Create UI
        self.setup_ui()
        
        # Start with first step
        self.show_step(0)
        
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        """Setup setup wizard UI"""
        # Header
        self.header_frame = tk.Frame(self.window, bg='#3498db', height=80)
        self.header_frame.pack(fill=tk.X)
        self.header_frame.pack_propagate(False)
        
        self.title_label = tk.Label(
            self.header_frame,
            text="",
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#3498db'
        )
        self.title_label.pack(expand=True)
        
        self.subtitle_label = tk.Label(
            self.header_frame,
            text="",
            font=('Arial', 12),
            fg='#ecf0f1',
            bg='#3498db'
        )
        self.subtitle_label.pack(expand=True)
        
        # Content area
        self.content_frame = tk.Frame(self.window, bg='#ecf0f1')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Progress bar
        self.progress_frame = tk.Frame(self.window, bg='#2c3e50', height=30)
        self.progress_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.progress_frame.pack_propagate(False)
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            length=400
        )
        self.progress_bar.pack(pady=5)
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="",
            font=('Arial', 9),
            fg='white',
            bg='#2c3e50'
        )
        self.progress_label.pack()
        
        # Navigation buttons
        self.nav_frame = tk.Frame(self.window, bg='#2c3e50', height=60)
        self.nav_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.nav_frame.pack_propagate(False)
        
        self.button_frame = tk.Frame(self.nav_frame, bg='#2c3e50')
        self.button_frame.pack(expand=True)
        
        self.back_button = tk.Button(
            self.button_frame,
            text="← Back",
            font=('Arial', 11),
            bg='#7f8c8d',
            fg='white',
            padx=20,
            pady=8,
            state=tk.DISABLED,
            command=self.previous_step
        )
        self.back_button.pack(side=tk.LEFT, padx=10)
        
        self.next_button = tk.Button(
            self.button_frame,
            text="Next →",
            font=('Arial', 11),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=8,
            command=self.next_step
        )
        self.next_button.pack(side=tk.LEFT, padx=10)
        
        self.cancel_button = tk.Button(
            self.button_frame,
            text="Cancel",
            font=('Arial', 11),
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=8,
            command=self.cancel_setup
        )
        self.cancel_button.pack(side=tk.LEFT, padx=10)
        
    def show_step(self, step_index):
        """Show a specific step"""
        self.current_step = step_index
        
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Update progress
        progress_value = int((step_index + 1) / len(self.steps) * 100)
        self.progress_bar['value'] = progress_value
        self.progress_label.config(text=f"Step {step_index + 1} of {len(self.steps)}")
        
        # Show step
        self.steps[step_index]()
        
        # Update navigation buttons
        self.back_button.config(state=tk.NORMAL if step_index > 0 else tk.DISABLED)
        
        if step_index == len(self.steps) - 1:
            self.next_button.config(text="Finish", bg='#2ecc71')
        else:
            self.next_button.config(text="Next →", bg='#3498db')
            
    def step_welcome(self):
        """Welcome step"""
        self.title_label.config(text="Welcome to Python OS")
        self.subtitle_label.config(text="Let's set up your system")
        
        welcome_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        welcome_frame.pack(expand=True)
        
        # Welcome icon
        icon_label = tk.Label(
            welcome_frame,
            text="🚀",
            font=('Arial', 72),
            bg='#ecf0f1'
        )
        icon_label.pack(pady=(20, 30))
        
        # Welcome message
        message = tk.Label(
            welcome_frame,
            text="""Thank you for choosing Python OS!

This setup will guide you through configuring your new
operating system. It should only take a few minutes.

We'll set up:
• Your user account
• System preferences
• Privacy settings
• Initial applications

Click 'Next' to continue.""",
            font=('Arial', 13),
            bg='#ecf0f1',
            justify=tk.CENTER
        )
        message.pack(pady=10)
        
    def step_license(self):
        """License agreement step"""
        self.title_label.config(text="License Agreement")
        self.subtitle_label.config(text="Please read and accept the terms")
        
        # License text
        license_text = """PYTHON OS SIMULATOR END USER LICENSE AGREEMENT

1. GRANT OF LICENSE
This Python OS Simulator is provided as-is for educational
and demonstration purposes. You may use, modify, and
distribute this software for non-commercial purposes.

2. RESTRICTIONS
You may not:
- Use this software for illegal purposes
- Claim this software as your own work
- Redistribute without attribution

3. DISCLAIMER
This software is provided "as is" without warranty of any
kind. The developers are not liable for any damages
resulting from the use of this software.

4. PRIVACY
This simulator may collect usage data for improvement
purposes. No personal information is collected.

By proceeding, you agree to these terms."""
        
        # Text widget with scrollbar
        text_frame = tk.Frame(self.content_frame, bg='white')
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        text_widget = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=('Courier New', 10),
            bg='white',
            fg='black',
            height=15
        )
        text_widget.insert(1.0, license_text)
        text_widget.config(state=tk.DISABLED)
        
        scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Agreement checkbox
        self.agree_var = tk.BooleanVar(value=False)
        agree_check = tk.Checkbutton(
            self.content_frame,
            text="I accept the license agreement",
            variable=self.agree_var,
            font=('Arial', 11),
            bg='#ecf0f1'
        )
        agree_check.pack(pady=20)
        
    def step_user_account(self):
        """User account creation step"""
        self.title_label.config(text="Create User Account")
        self.subtitle_label.config(text="Set up your administrator account")
        
        form_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        form_frame.pack(expand=True)
        
        # Full Name
        tk.Label(
            form_frame,
            text="Full Name:",
            font=('Arial', 12),
            bg='#ecf0f1',
            anchor=tk.W
        ).pack(fill=tk.X, pady=(20, 5))
        
        self.name_entry = tk.Entry(
            form_frame,
            font=('Arial', 12),
            width=40
        )
        self.name_entry.pack(pady=(0, 15))
        self.name_entry.insert(0, "Administrator")
        self.name_entry.bind('<KeyRelease>', lambda e: self.update_username())
        
        # Username
        tk.Label(
            form_frame,
            text="Username:",
            font=('Arial', 12),
            bg='#ecf0f1',
            anchor=tk.W
        ).pack(fill=tk.X, pady=(0, 5))
        
        self.username_entry = tk.Entry(
            form_frame,
            font=('Arial', 12),
            width=40
        )
        self.username_entry.pack(pady=(0, 15))
        self.username_entry.insert(0, "admin")
        
        # Password
        tk.Label(
            form_frame,
            text="Password:",
            font=('Arial', 12),
            bg='#ecf0f1',
            anchor=tk.W
        ).pack(fill=tk.X, pady=(0, 5))
        
        self.password_entry = tk.Entry(
            form_frame,
            font=('Arial', 12),
            width=40,
            show="●"
        )
        self.password_entry.pack(pady=(0, 10))
        
        # Password confirmation
        tk.Label(
            form_frame,
            text="Confirm Password:",
            font=('Arial', 12),
            bg='#ecf0f1',
            anchor=tk.W
        ).pack(fill=tk.X, pady=(0, 5))
        
        self.confirm_entry = tk.Entry(
            form_frame,
            font=('Arial', 12),
            width=40,
            show="●"
        )
        self.confirm_entry.pack(pady=(0, 10))
        
        # Error label
        self.user_error = tk.Label(
            form_frame,
            text="",
            font=('Arial', 10),
            fg='#e74c3c',
            bg='#ecf0f1'
        )
        self.user_error.pack()
        
    def update_username(self):
        """Update username based on full name"""
        full_name = self.name_entry.get()
        if full_name:
            # Generate username from full name
            username = full_name.lower().replace(' ', '.')
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, username)
            
    def step_computer_name(self):
        """Computer name step"""
        self.title_label.config(text="Computer Name")
        self.subtitle_label.config(text="Give your computer a name")
        
        form_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        form_frame.pack(expand=True)
        
        tk.Label(
            form_frame,
            text="Computer Name:",
            font=('Arial', 14, 'bold'),
            bg='#ecf0f1'
        ).pack(pady=(40, 10))
        
        tk.Label(
            form_frame,
            text="This name will identify your computer on the network.",
            font=('Arial', 11),
            bg='#ecf0f1',
            fg='#7f8c8d'
        ).pack(pady=(0, 20))
        
        self.computer_entry = tk.Entry(
            form_frame,
            font=('Arial', 14),
            width=30
        )
        self.computer_entry.pack(pady=10)
        self.computer_entry.insert(0, "PythonOS-PC")
        
        # Example names
        example_frame = tk.Frame(form_frame, bg='#ecf0f1')
        example_frame.pack(pady=20)
        
        tk.Label(
            example_frame,
            text="Examples:",
            font=('Arial', 11, 'italic'),
            bg='#ecf0f1',
            fg='#7f8c8d'
        ).pack(anchor=tk.W)
        
        examples = ["MyPythonPC", "Development-Machine", "PythonOS-Workstation"]
        for example in examples:
            tk.Label(
                example_frame,
                text=f"• {example}",
                font=('Arial', 10),
                bg='#ecf0f1',
                fg='#7f8c8d'
            ).pack(anchor=tk.W)
            
    def step_timezone(self):
        """Timezone selection step"""
        self.title_label.config(text="Time and Date")
        self.subtitle_label.config(text="Select your timezone")
        
        form_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Map frame
        map_frame = tk.Frame(form_frame, bg='white', relief=tk.SUNKEN, borderwidth=2)
        map_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Simplified world map (text-based)
        map_text = """
                    WORLD TIMEZONES
        ┌─────────────────────────────────────┐
        │                                     │
        │  (UTC-8) Los Angeles  (UTC-5) New York │
        │                                     │
        │  (UTC) London        (UTC+1) Paris │
        │                                     │
        │  (UTC+3) Moscow      (UTC+8) Beijing│
        │                                     │
        │  (UTC+9) Tokyo       (UTC+10) Sydney│
        │                                     │
        └─────────────────────────────────────┘
        """
        
        tk.Label(
            map_frame,
            text=map_text,
            font=('Courier New', 10),
            bg='white',
            justify=tk.LEFT
        ).pack(pady=20)
        
        # Timezone selection
        tz_frame = tk.Frame(form_frame, bg='#ecf0f1')
        tz_frame.pack(fill=tk.X)
        
        tk.Label(
            tz_frame,
            text="Select your timezone:",
            font=('Arial', 12),
            bg='#ecf0f1'
        ).pack(anchor=tk.W, pady=(0, 10))
        
        timezones = [
            "UTC-8:00 (Pacific Time)",
            "UTC-5:00 (Eastern Time)", 
            "UTC+0:00 (London)",
            "UTC+1:00 (Central Europe)",
            "UTC+3:00 (Moscow)",
            "UTC+5:30 (India)",
            "UTC+8:00 (China)",
            "UTC+9:00 (Japan)",
            "UTC+10:00 (Australia)"
        ]
        
        self.tz_var = tk.StringVar(value=timezones[2])
        tz_combo = ttk.Combobox(
            tz_frame,
            textvariable=self.tz_var,
            values=timezones,
            state='readonly',
            width=40
        )
        tz_combo.pack()
        
        # Current time display
        time_frame = tk.Frame(form_frame, bg='#ecf0f1')
        time_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.time_label = tk.Label(
            time_frame,
            text="",
            font=('Arial', 12),
            bg='#ecf0f1'
        )
        self.time_label.pack()
        
        # Update time display
        self.update_time_display()
        
    def update_time_display(self):
        """Update time display based on selected timezone"""
        import datetime
        now = datetime.datetime.utcnow()
        
        # Extract UTC offset from selection
        tz_str = self.tz_var.get()
        if "UTC-" in tz_str:
            offset = -int(tz_str.split('-')[1].split(':')[0])
        elif "UTC+" in tz_str:
            offset = int(tz_str.split('+')[1].split(':')[0])
        else:
            offset = 0
            
        local_time = now + datetime.timedelta(hours=offset)
        time_str = local_time.strftime("%Y-%m-%d %H:%M:%S")
        
        self.time_label.config(text=f"Local time will be: {time_str}")
        self.window.after(1000, self.update_time_display)
        
    def step_theme(self):
        """Theme selection step"""
        self.title_label.config(text="Choose Your Style")
        self.subtitle_label.config(text="Select a theme for your desktop")
        
        # Theme previews
        themes = [
            {
                'id': 'default',
                'name': 'Default',
                'bg': '#2c3e50',
                'fg': '#ecf0f1',
                'accent': '#3498db',
                'desc': 'Balanced dark theme'
            },
            {
                'id': 'dark',
                'name': 'Dark',
                'bg': '#1e1e1e',
                'fg': '#d4d4d4',
                'accent': '#007acc',
                'desc': 'Developer-friendly dark theme'
            },
            {
                'id': 'light',
                'name': 'Light',
                'bg': '#ffffff',
                'fg': '#000000',
                'accent': '#007acc',
                'desc': 'Clean light theme'
            },
            {
                'id': 'blue',
                'name': 'Ocean Blue',
                'bg': '#1c2833',
                'fg': '#d6dbdf',
                'accent': '#3498db',
                'desc': 'Deep blue theme'
            }
        ]
        
        # Theme selection frame
        theme_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        theme_frame.pack(fill=tk.BOTH, expand=True)
        
        self.theme_var = tk.StringVar(value='default')
        
        # Create theme previews
        for i, theme in enumerate(themes):
            theme_preview = tk.Frame(
                theme_frame,
                bg='white',
                relief=tk.RAISED,
                borderwidth=2
            )
            theme_preview.grid(row=i//2, column=i%2, padx=10, pady=10, sticky='nsew')
            
            # Make grid expandable
            theme_frame.grid_rowconfigure(i//2, weight=1)
            theme_frame.grid_columnconfigure(i%2, weight=1)
            
            # Theme color preview
            color_frame = tk.Frame(theme_preview, bg=theme['bg'], height=60)
            color_frame.pack(fill=tk.X)
            
            # Theme name
            tk.Label(
                theme_preview,
                text=theme['name'],
                font=('Arial', 12, 'bold'),
                bg='white'
            ).pack(pady=(10, 5))
            
            # Theme description
            tk.Label(
                theme_preview,
                text=theme['desc'],
                font=('Arial', 10),
                bg='white',
                wraplength=150
            ).pack(pady=(0, 10))
            
            # Radio button
            tk.Radiobutton(
                theme_preview,
                text="Select",
                variable=self.theme_var,
                value=theme['id'],
                bg='white'
            ).pack(pady=(0, 10))
            
            # Bind click on entire frame
            theme_preview.bind('<Button-1>', 
                lambda e, t=theme['id']: self.theme_var.set(t))
                
        # Wallpaper selection
        wall_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        wall_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Label(
            wall_frame,
            text="Choose wallpaper:",
            font=('Arial', 12),
            bg='#ecf0f1'
        ).pack(anchor=tk.W, pady=(0, 10))
        
        wall_btn_frame = tk.Frame(wall_frame, bg='#ecf0f1')
        wall_btn_frame.pack()
        
        wallpapers = ['Default', 'Nature', 'Abstract', 'Solid Color', 'Custom']
        self.wall_var = tk.StringVar(value='Default')
        
        for wall in wallpapers:
            tk.Radiobutton(
                wall_btn_frame,
                text=wall,
                variable=self.wall_var,
                value=wall,
                bg='#ecf0f1'
            ).pack(side=tk.LEFT, padx=10)
            
    def step_privacy(self):
        """Privacy settings step"""
        self.title_label.config(text="Privacy Settings")
        self.subtitle_label.config(text="Choose your privacy preferences")
        
        privacy_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        privacy_frame.pack(fill=tk.BOTH, expand=True)
        
        # Privacy options
        options = [
            ("Send usage statistics", 
             "Help improve Python OS by sending anonymous usage data", True),
            ("Error reporting", 
             "Automatically send crash reports to developers", True),
            ("Check for updates automatically",
             "Periodically check for system updates", True),
            ("Location services",
             "Allow applications to access location (simulated)", False),
            ("Diagnostic data",
             "Send diagnostic data about system performance", False)
        ]
        
        self.privacy_vars = []
        
        for i, (title, desc, default) in enumerate(options):
            var = tk.BooleanVar(value=default)
            self.privacy_vars.append((title, var))
            
            option_frame = tk.Frame(privacy_frame, bg='#ecf0f1')
            option_frame.pack(fill=tk.X, pady=5)
            
            check = tk.Checkbutton(
                option_frame,
                text=title,
                variable=var,
                font=('Arial', 11, 'bold'),
                bg='#ecf0f1'
            )
            check.pack(anchor=tk.W)
            
            tk.Label(
                option_frame,
                text=desc,
                font=('Arial', 10),
                bg='#ecf0f1',
                fg='#7f8c8d',
                wraplength=500
            ).pack(anchor=tk.W, padx=20)
            
    def step_install_apps(self):
        """Application installation step"""
        self.title_label.config(text="Install Applications")
        self.subtitle_label.config(text="Choose which applications to install")
        
        apps_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        apps_frame.pack(fill=tk.BOTH, expand=True)
        
        # Available applications
        apps = [
            ("Web Browser", "Browse the simulated internet", True),
            ("Media Player", "Play music and videos", True),
            ("Text Editor", "Edit text files with syntax highlighting", True),
            ("Calculator", "Scientific calculator", True),
            ("Calendar", "Desktop calendar with reminders", False),
            ("Photo Viewer", "View and edit images", False),
            ("Terminal", "Command line interface (required)", True),
            ("File Explorer", "File management (required)", True)
        ]
        
        self.app_vars = []
        
        # Scrollable frame
        canvas = tk.Canvas(apps_frame, bg='#ecf0f1', highlightthickness=0)
        scrollbar = tk.Scrollbar(apps_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ecf0f1')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for i, (name, desc, default) in enumerate(apps):
            var = tk.BooleanVar(value=default)
            self.app_vars.append((name, var))
            
            app_frame = tk.Frame(scrollable_frame, bg='white', relief=tk.RAISED, borderwidth=1)
            app_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Checkbox and app info
            check = tk.Checkbutton(
                app_frame,
                text=name,
                variable=var,
                font=('Arial', 11, 'bold'),
                bg='white'
            )
            check.pack(anchor=tk.W, padx=10, pady=5)
            
            tk.Label(
                app_frame,
                text=desc,
                font=('Arial', 10),
                bg='white',
                fg='#7f8c8d'
            ).pack(anchor=tk.W, padx=30, pady=(0, 5))
            
            # Disable required apps
            if "required" in desc.lower():
                check.config(state=tk.DISABLED)
                
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def step_final(self):
        """Final step - summary and installation"""
        self.title_label.config(text="Ready to Install")
        self.subtitle_label.config(text="Review your settings")
        
        summary_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        summary_frame.pack(fill=tk.BOTH, expand=True)
        
        # Summary text
        summary_text = f"""
        Summary of your configuration:
        
        User Account: {self.setup_data.get('user_name', 'Not set')}
        Computer Name: {self.setup_data.get('computer_name', 'Not set')}
        Timezone: {self.setup_data.get('timezone', 'Not set')}
        Theme: {self.setup_data.get('theme', 'Not set')}
        
        Applications to install: {sum(1 for _, var in self.app_vars if var.get())}
        Privacy settings configured: Yes
        
        Total space required: ~150 MB
        Estimated time: 1-2 minutes
        """
        
        tk.Label(
            summary_frame,
            text=summary_text,
            font=('Courier New', 11),
            bg='#ecf0f1',
            justify=tk.LEFT
        ).pack(pady=20)
        
        # Installation notes
        notes_frame = tk.Frame(summary_frame, bg='#fff9c4', relief=tk.SUNKEN, borderwidth=1)
        notes_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            notes_frame,
            text="⚠️ Important Notes:",
            font=('Arial', 11, 'bold'),
            bg='#fff9c4'
        ).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        notes = [
            "• Your system will restart after installation",
            "• Do not turn off power during setup",
            "• You can change most settings later in System Settings",
            "• Internet connection is not required for this simulator"
        ]
        
        for note in notes:
            tk.Label(
                notes_frame,
                text=note,
                font=('Arial', 10),
                bg='#fff9c4',
                anchor=tk.W
            ).pack(anchor=tk.W, padx=20, pady=2)
            
    def validate_step(self):
        """Validate current step"""
        if self.current_step == 1:  # License
            if not self.agree_var.get():
                messagebox.showwarning("License Required", 
                                     "You must accept the license agreement to continue.")
                return False
                
        elif self.current_step == 2:  # User account
            name = self.name_entry.get().strip()
            username = self.username_entry.get().strip()
            password = self.password_entry.get()
            confirm = self.confirm_entry.get()
            
            if not name:
                self.user_error.config(text="Please enter your full name")
                return False
            if not username:
                self.user_error.config(text="Please enter a username")
                return False
            if not password:
                self.user_error.config(text="Please enter a password")
                return False
            if password != confirm:
                self.user_error.config(text="Passwords do not match")
                return False
            if len(password) < 4:
                self.user_error.config(text="Password must be at least 4 characters")
                return False
                
            # Save user data
            self.setup_data['user_name'] = name
            self.setup_data['user_username'] = username
            self.setup_data['user_password'] = password
            self.user_error.config(text="")
            
        elif self.current_step == 3:  # Computer name
            computer_name = self.computer_entry.get().strip()
            if not computer_name:
                messagebox.showwarning("Computer Name Required",
                                     "Please enter a computer name.")
                return False
            self.setup_data['computer_name'] = computer_name
            
        elif self.current_step == 4:  # Timezone
            self.setup_data['timezone'] = self.tz_var.get()
            
        elif self.current_step == 5:  # Theme
            self.setup_data['theme'] = self.theme_var.get()
            self.setup_data['wallpaper'] = self.wall_var.get()
            
        elif self.current_step == 6:  # Privacy
            privacy_settings = {}
            for title, var in self.privacy_vars:
                key = title.lower().replace(' ', '_')
                privacy_settings[key] = var.get()
            self.setup_data['privacy'] = privacy_settings
            
        elif self.current_step == 7:  # Apps
            apps_to_install = []
            for name, var in self.app_vars:
                if var.get():
                    apps_to_install.append(name)
            self.setup_data['apps_to_install'] = apps_to_install
            
        return True
        
    def next_step(self):
        """Go to next step"""
        if not self.validate_step():
            return
            
        if self.current_step == len(self.steps) - 1:
            # Final step - complete setup
            self.complete_setup()
        else:
            self.show_step(self.current_step + 1)
            
    def previous_step(self):
        """Go to previous step"""
        self.show_step(self.current_step - 1)
        
    def cancel_setup(self):
        """Cancel setup process"""
        if messagebox.askyesno("Cancel Setup", 
                             "Are you sure you want to cancel setup?\nThe system will shut down."):
            self.os_app.show_shutdown_screen()
            self.window.destroy()
            
    def complete_setup(self):
        """Complete the setup process"""
        self.title_label.config(text="Installing Python OS...")
        self.subtitle_label.config(text="Please wait while we set up your system")
        
        # Disable navigation
        self.back_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.DISABLED)
        
        # Show installation progress
        self.show_installation_progress()
        
    def show_installation_progress(self):
        """Show installation progress animation"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Installation frame
        install_frame = tk.Frame(self.content_frame, bg='#ecf0f1')
        install_frame.pack(expand=True)
        
        # Spinner/loading animation
        self.spinner_label = tk.Label(
            install_frame,
            text="⏳",
            font=('Arial', 48),
            bg='#ecf0f1'
        )
        self.spinner_label.pack(pady=20)
        
        # Status label
        self.install_status = tk.Label(
            install_frame,
            text="Starting installation...",
            font=('Arial', 14),
            bg='#ecf0f1'
        )
        self.install_status.pack(pady=10)
        
        # Detailed progress
        self.install_details = tk.Label(
            install_frame,
            text="",
            font=('Courier New', 10),
            bg='#ecf0f1',
            justify=tk.LEFT
        )
        self.install_details.pack(pady=10)
        
        # Progress bar
        self.install_progress = ttk.Progressbar(
            install_frame,
            mode='determinate',
            length=400
        )
        self.install_progress.pack(pady=20)
        
        # Start installation process
        self.install_steps()
        
    def install_steps(self):
        """Execute installation steps"""
        steps = [
            ("Creating user account...", 10, self.create_user_account),
            ("Configuring system settings...", 20, self.configure_system),
            ("Applying theme...", 30, self.apply_theme),
            ("Installing applications...", 60, self.install_applications),
            ("Finalizing setup...", 90, self.finalize_setup),
            ("Completing installation...", 100, self.finish_installation)
        ]
        
        self.current_install_step = 0
        
        def execute_next_step():
            if self.current_install_step < len(steps):
                message, progress, func = steps[self.current_install_step]
                self.install_status.config(text=message)
                self.install_progress['value'] = progress
                
                # Update spinner
                spinners = ["⏳", "⌛", "⏳", "⌛"]
                self.spinner_label.config(text=spinners[self.current_install_step % 4])
                
                # Execute step
                result = func()
                self.install_details.config(text=result)
                
                self.current_install_step += 1
                self.window.after(1000, execute_next_step)
            else:
                # Installation complete
                self.install_complete()
                
        execute_next_step()
        
    def create_user_account(self):
        """Create user account"""
        try:
            # Hash password
            import hashlib
            password_hash = hashlib.sha256(
                self.setup_data['user_password'].encode()
            ).hexdigest()
            
            # Create user in database
            self.os_app.db.connect()
            self.os_app.db.cursor.execute('''
                INSERT OR REPLACE INTO users 
                (username, password, full_name, is_admin)
                VALUES (?, ?, ?, ?)
            ''', (
                self.setup_data['user_username'],
                password_hash,
                self.setup_data['user_name'],
                1
            ))
            
            # Set as current user
            self.os_app.current_user = self.setup_data['user_username']
            
            self.os_app.db.connection.commit()
            return "✓ User account created successfully"
        except Exception as e:
            return f"✗ Error creating user: {str(e)}"
            
    def configure_system(self):
        """Configure system settings"""
        try:
            # Create system_info table
            self.os_app.db.cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_info (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')
            
            # Store setup data
            settings = [
                ('setup_completed', 'true'),
                ('setup_timestamp', str(time.time())),
                ('computer_name', self.setup_data['computer_name']),
                ('timezone', self.setup_data['timezone']),
                ('version', '2.0'),
                ('build', '2024.01')
            ]
            
            for key, value in settings:
                self.os_app.db.cursor.execute('''
                    INSERT OR REPLACE INTO system_info (key, value)
                    VALUES (?, ?)
                ''', (key, value))
                
            # Store privacy settings
            for key, value in self.setup_data['privacy'].items():
                self.os_app.db.cursor.execute('''
                    INSERT OR REPLACE INTO settings (user_id, setting_key, setting_value)
                    SELECT id, ?, ? FROM users WHERE username = ?
                ''', (key, str(value), self.os_app.current_user))
                
            self.os_app.db.connection.commit()
            return "✓ System configured successfully"
        except Exception as e:
            return f"✗ Error configuring system: {str(e)}"
            
    def apply_theme(self):
        """Apply selected theme"""
        try:
            # Set theme
            self.os_app.theme_manager.set_theme(self.setup_data['theme'])
            
            # Store theme preference
            self.os_app.db.cursor.execute('''
                INSERT OR REPLACE INTO settings (user_id, setting_key, setting_value)
                SELECT id, 'theme', ? FROM users WHERE username = ?
            ''', (self.setup_data['theme'], self.os_app.current_user))
            
            # Store wallpaper preference
            self.os_app.db.cursor.execute('''
                INSERT OR REPLACE INTO settings (user_id, setting_key, setting_value)
                SELECT id, 'wallpaper', ? FROM users WHERE username = ?
            ''', (self.setup_data['wallpaper'], self.os_app.current_user))
            
            self.os_app.db.connection.commit()
            return f"✓ Applied {self.setup_data['theme']} theme"
        except Exception as e:
            return f"✗ Error applying theme: {str(e)}"
            
    def install_applications(self):
        """Install selected applications"""
        try:
            apps_installed = 0
            app_list = self.setup_data.get('apps_to_install', [])
            
            for app_name in app_list:
                # Mark as installed in database
                self.os_app.db.cursor.execute('''
                    UPDATE installed_apps SET is_system_app = 1
                    WHERE name = ? AND is_system_app = 0
                ''', (app_name,))
                apps_installed += 1
                
                # Simulate installation delay
                time.sleep(0.1)
                
            self.os_app.db.connection.commit()
            
            # Reload installed apps
            self.os_app.installed_apps = self.os_app.load_installed_apps()
            
            return f"✓ Installed {apps_installed} applications"
        except Exception as e:
            return f"✗ Error installing applications: {str(e)}"
            
    def finalize_setup(self):
        """Finalize setup"""
        try:
            # Create welcome file
            welcome_content = f"""Welcome to Python OS, {self.setup_data['user_name']}!

Your system has been successfully configured:

Computer Name: {self.setup_data['computer_name']}
Timezone: {self.setup_data['timezone']}
Theme: {self.setup_data['theme']}

Thank you for choosing Python OS!
"""
            
            self.os_app.db.cursor.execute('''
                INSERT OR REPLACE INTO filesystem (name, type, path, content)
                VALUES (?, 'file', '/home/admin', ?)
            ''', ('welcome.txt', welcome_content))
            
            self.os_app.db.connection.commit()
            return "✓ Created welcome files"
        except Exception as e:
            return f"✗ Error finalizing: {str(e)}"
            
    def finish_installation(self):
        """Finish installation"""
        return "✓ Installation complete!"
        
    def install_complete(self):
        """Handle installation completion"""
        self.install_status.config(text="Installation Complete!")
        self.spinner_label.config(text="✓")
        self.install_details.config(text="Your system is ready to use.")
        
        # Show completion message
        self.window.after(2000, self.show_completion)
        
    def show_completion(self):
        """Show completion screen"""
        # Clear everything
        for widget in self.window.winfo_children():
            widget.destroy()
            
        # Completion screen
        completion_frame = tk.Frame(self.window, bg='#2c3e50')
        completion_frame.pack(fill=tk.BOTH, expand=True)
        
        # Success icon
        tk.Label(
            completion_frame,
            text="🎉",
            font=('Arial', 72),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=40)
        
        # Success message
        tk.Label(
            completion_frame,
            text="Python OS Setup Complete!",
            font=('Arial', 24, 'bold'),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=10)
        
        tk.Label(
            completion_frame,
            text="Your system is now ready to use.",
            font=('Arial', 14),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack(pady=10)
        
        # Details
        details = f"""
        System configured for: {self.setup_data['user_name']}
        Computer: {self.setup_data['computer_name']}
        Theme: {self.setup_data['theme']}
        
        You can now log in with your new account.
        """
        
        tk.Label(
            completion_frame,
            text=details,
            font=('Courier New', 11),
            bg='#34495e',
            fg='white',
            justify=tk.LEFT,
            padx=20,
            pady=20
        ).pack(pady=20, fill=tk.X, padx=50)
        
        # Restart button
        restart_btn = tk.Button(
            completion_frame,
            text="Restart Now",
            font=('Arial', 14, 'bold'),
            bg='#2ecc71',
            fg='white',
            padx=30,
            pady=15,
            command=self.restart_system
        )
        restart_btn.pack(pady=30)
        
        # Set first boot flag to False
        self.os_app.first_boot = False
        
    def restart_system(self):
        """Restart the system after setup"""
        self.window.destroy()
        self.os_app.restart_system()