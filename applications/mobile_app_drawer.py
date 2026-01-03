# applications/mobile_app_drawer.py
import tkinter as tk
from tkinter import ttk
import math

class AppDrawer:
    def __init__(self, parent, os_app, apps):
        self.os_app = os_app
        self.parent = parent
        self.apps = apps
        
        # Create drawer window
        self.window = tk.Toplevel(parent)
        self.window.title("Apps")
        self.window.geometry("360x600")
        self.window.configure(bg='#121212')
        
        # Make it modal-like
        self.window.transient(parent)
        self.window.grab_set()
        
        # Setup drawer
        self.setup_drawer()
        
    def setup_drawer(self):
        """Setup app drawer interface"""
        # Header
        header_frame = tk.Frame(self.window, bg='#1a1a1a', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="Apps",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#1a1a1a'
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        # Close button
        close_btn = tk.Label(
            header_frame,
            text="✕",
            font=('Arial', 24),
            fg='white',
            bg='#1a1a1a',
            cursor='hand2'
        )
        close_btn.pack(side=tk.RIGHT, padx=20)
        close_btn.bind('<Button-1>', lambda e: self.window.destroy())
        
        # Search bar
        search_frame = tk.Frame(self.window, bg='#121212', padx=20, pady=10)
        search_frame.pack(fill=tk.X)
        
        search_entry = tk.Entry(
            search_frame,
            font=('Arial', 14),
            bg='#2a2a2a',
            fg='white',
            insertbackground='white'
        )
        search_entry.pack(fill=tk.X, ipady=8)
        search_entry.insert(0, "Search apps...")
        
        # App grid
        self.setup_app_grid()
        
    def setup_app_grid(self):
        """Setup app grid in drawer"""
        # Container for apps
        canvas = tk.Canvas(self.window, bg='#121212', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#121212')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Organize apps alphabetically
        sorted_apps = sorted(self.apps, key=lambda x: x[0])
        
        # Create 4-column grid
        cols = 4
        rows = math.ceil(len(sorted_apps) / cols)
        
        for i, (name, icon, command, color) in enumerate(sorted_apps):
            row = i // cols
            col = i % cols
            
            self.create_drawer_app(scrollable_frame, name, icon, command, color, row, col)
            
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_drawer_app(self, parent, name, icon, command, color, row, col):
        """Create app button in drawer"""
        frame = tk.Frame(parent, bg='#121212', width=80, height=100)
        frame.grid(row=row, column=col, padx=5, pady=5)
        
        # Icon background
        icon_frame = tk.Frame(
            frame,
            bg=color,
            width=60,
            height=60,
            relief=tk.FLAT
        )
        icon_frame.pack(pady=(5, 5))
        
        # Icon
        icon_label = tk.Label(
            icon_frame,
            text=icon,
            font=('Arial', 24),
            bg=color,
            fg='white'
        )
        icon_label.pack(expand=True)
        
        # App name
        name_label = tk.Label(
            frame,
            text=name,
            font=('Arial', 9),
            fg='white',
            bg='#121212',
            wraplength=70
        )
        name_label.pack()
        
        # Bind click events
        icon_frame.bind('<Button-1>', lambda e: self.launch_app(command))
        icon_label.bind('<Button-1>', lambda e: self.launch_app(command))
        name_label.bind('<Button-1>', lambda e: self.launch_app(command))
        
    def launch_app(self, command):
        """Launch app and close drawer"""
        self.window.destroy()
        command()