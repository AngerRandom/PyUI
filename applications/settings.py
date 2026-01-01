# applications/settings.py
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
        """Setup system settings"""
        tk.Label(parent, text="System Information:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        info_frame = tk.Frame(parent)
        info_frame.pack(fill=tk.X, padx=40, pady=10)
        
        info = [
            ("OS Version:", "Python OS Simulator 1.0"),
            ("User:", self.os_app.current_user),
            ("Database:", "SQLite 3.0"),
            ("UI Framework:", "Tkinter"),
            ("Python:", "3.x")
        ]
        
        for label, value in info:
            frame = tk.Frame(info_frame)
            frame.pack(fill=tk.X, pady=2)
            
            tk.Label(frame, text=label, width=15, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(frame, text=value).pack(side=tk.LEFT)
            
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
