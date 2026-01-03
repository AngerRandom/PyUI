# applications/mobile_browser.py
import tkinter as tk
from tkinter import ttk, messagebox

class MobileBrowser:
    def __init__(self, parent, os_app):
        self.os_app = os_app
        self.parent = parent
        self.history = []
        self.current_url = "about:home"
        
        # Create browser window
        self.window = tk.Toplevel(parent)
        self.window.title("Browser")
        self.window.geometry("360x600")
        
        self.setup_browser()
        self.load_url(self.current_url)
        
    def setup_browser(self):
        """Setup mobile browser interface"""
        # Header with URL bar
        header_frame = tk.Frame(self.window, bg='#2196F3', height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Navigation buttons
        nav_frame = tk.Frame(header_frame, bg='#2196F3')
        nav_frame.pack(fill=tk.X, padx=10, pady=5)
        
        buttons = [
            ("‹", self.go_back),
            ("›", self.go_forward),
            ("↻", self.refresh),
            ("✕", self.window.destroy)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                nav_frame,
                text=text,
                font=('Arial', 14),
                bg='#1976D2',
                fg='white',
                width=3,
                command=command
            )
            btn.pack(side=tk.LEFT, padx=2)
            
        # URL bar
        url_frame = tk.Frame(header_frame, bg='#2196F3')
        url_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.url_var = tk.StringVar()
        self.url_entry = tk.Entry(
            url_frame,
            textvariable=self.url_var,
            font=('Arial', 12),
            bg='white',
            fg='black'
        )
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        self.url_entry.bind('<Return>', lambda e: self.load_url(self.url_var.get()))
        
        go_btn = tk.Button(
            url_frame,
            text="Go",
            font=('Arial', 12),
            bg='#4CAF50',
            fg='white',
            command=lambda: self.load_url(self.url_var.get())
        )
        go_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Browser content
        self.content_frame = tk.Frame(self.window, bg='white')
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
    def load_url(self, url):
        """Load a URL"""
        if not url.startswith(('http://', 'https://', 'about:')):
            url = 'https://' + url
            
        self.current_url = url
        self.url_var.set(url)
        self.history.append(url)
        
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Load page
        if url == "about:home":
            self.show_home_page()
        elif url == "about:bookmarks":
            self.show_bookmarks()
        else:
            self.show_web_page(url)
            
    def show_home_page(self):
        """Show browser home page"""
        content = """
        Python OS Mobile Browser
        
        Quick Links:
        • python.org
        • github.com
        • news.example.com
        
        Mobile-optimized browsing
        """
        
        tk.Label(
            self.content_frame,
            text=content,
            font=('Arial', 14),
            bg='white',
            fg='black',
            justify=tk.LEFT,
            wraplength=300
        ).pack(pady=50, padx=20)
        
    def show_web_page(self, url):
        """Show web page content"""
        # Simulate web page
        domain = url.split('//')[-1].split('/')[0]
        
        if 'python.org' in domain:
            content = """
            Welcome to Python.org
            
            Python is a programming language
            that lets you work quickly and
            integrate systems more effectively.
            
            (Mobile-optimized view)
            """
        elif 'github.com' in domain:
            content = """
            GitHub Mobile
            
            Where the world builds software.
            
            (Mobile-optimized view)
            """
        else:
            content = f"""
            {domain}
            
            Mobile web page simulation.
            
            URL: {url}
            
            (This is a simulated browser)
            """
            
        tk.Label(
            self.content_frame,
            text=content,
            font=('Arial', 12),
            bg='white',
            fg='black',
            justify=tk.LEFT,
            wraplength=300
        ).pack(pady=20, padx=20)
        
    def show_bookmarks(self):
        """Show bookmarks"""
        bookmarks = [
            ("Python", "https://python.org"),
            ("GitHub", "https://github.com"),
            ("News", "https://news.example.com"),
            ("Weather", "https://weather.example.com")
        ]
        
        for name, url in bookmarks:
            btn = tk.Button(
                self.content_frame,
                text=name,
                font=('Arial', 14),
                bg='#f0f0f0',
                fg='black',
                command=lambda u=url: self.load_url(u)
            )
            btn.pack(fill=tk.X, padx=20, pady=5, ipady=10)
            
    def go_back(self):
        """Go back in history"""
        if len(self.history) > 1:
            self.history.pop()
            previous = self.history[-1]
            self.load_url(previous)
            
    def go_forward(self):
        """Go forward in history"""
        # Simplified - would track forward history
        messagebox.showinfo("Forward", "Forward not available in simulation")
        
    def refresh(self):
        """Refresh current page"""
        self.load_url(self.current_url)