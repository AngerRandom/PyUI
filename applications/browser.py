# applications/browser.py
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import re

class Browser:
    def __init__(self, parent, os_app):
        self.os_app = os_app
        self.parent = parent
        self.history = []
        self.bookmarks = [
            ("Python OS Home", "about:home"),
            ("Python.org", "https://www.python.org"),
            ("Tkinter Docs", "https://docs.python.org/3/library/tkinter.html"),
            ("GitHub", "https://github.com"),
            ("Simulated News", "about:news")
        ]
        
        # Create browser window
        self.window = tk.Toplevel(parent)
        self.window.title("Web Browser")
        self.window.geometry("900x600")
        
        self.setup_ui()
        self.load_page("about:home")
        
    def setup_ui(self):
        """Setup browser UI"""
        # Navigation bar
        nav_frame = tk.Frame(self.window)
        nav_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Back button
        back_btn = tk.Button(
            nav_frame,
            text="←",
            font=('Arial', 12),
            width=3,
            command=self.go_back
        )
        back_btn.pack(side=tk.LEFT, padx=2)
        
        # Forward button
        forward_btn = tk.Button(
            nav_frame,
            text="→",
            font=('Arial', 12),
            width=3,
            command=self.go_forward
        )
        forward_btn.pack(side=tk.LEFT, padx=2)
        
        # Refresh button
        refresh_btn = tk.Button(
            nav_frame,
            text="↻",
            font=('Arial', 12),
            width=3,
            command=self.refresh_page
        )
        refresh_btn.pack(side=tk.LEFT, padx=2)
        
        # Home button
        home_btn = tk.Button(
            nav_frame,
            text="⌂",
            font=('Arial', 12),
            width=3,
            command=lambda: self.load_page("about:home")
        )
        home_btn.pack(side=tk.LEFT, padx=2)
        
        # Address bar
        self.url_var = tk.StringVar()
        self.url_entry = tk.Entry(
            nav_frame,
            textvariable=self.url_var,
            font=('Arial', 11)
        )
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.url_entry.bind('<Return>', lambda e: self.load_page(self.url_var.get()))
        
        # Go button
        go_btn = tk.Button(
            nav_frame,
            text="Go",
            font=('Arial', 11),
            command=lambda: self.load_page(self.url_var.get())
        )
        go_btn.pack(side=tk.LEFT, padx=2)
        
        # Bookmarks button
        bookmarks_btn = tk.Button(
            nav_frame,
            text="☆",
            font=('Arial', 12),
            width=3,
            command=self.show_bookmarks
        )
        bookmarks_btn.pack(side=tk.LEFT, padx=2)
        
        # Tabs
        self.tab_control = ttk.Notebook(self.window)
        self.tab_control.pack(fill=tk.BOTH, expand=True)
        
        # Create first tab
        self.create_tab("New Tab")
        
        # Status bar
        self.status_bar = tk.Label(
            self.window,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def create_tab(self, title):
        """Create a new browser tab"""
        tab_frame = tk.Frame(self.tab_control)
        self.tab_control.add(tab_frame, text=title)
        
        # Text widget as "browser"
        browser_text = tk.Text(
            tab_frame,
            wrap=tk.WORD,
            bg='white',
            fg='black'
        )
        browser_text.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(browser_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        browser_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=browser_text.yview)
        
        return browser_text
        
    def load_page(self, url):
        """Load a web page (simulated)"""
        if not url.startswith(('http://', 'https://', 'about:')):
            url = 'http://' + url
            
        self.url_var.set(url)
        self.history.append(url)
        
        current_tab = self.tab_control.nametowidget(self.tab_control.select())
        browser_text = current_tab.winfo_children()[0]
        browser_text.delete(1.0, tk.END)
        
        if url == "about:home":
            content = self.get_home_page()
        elif url == "about:news":
            content = self.get_news_page()
        elif url.startswith("about:"):
            content = f"<h1>About Page</h1><p>Internal page: {url}</p>"
        else:
            content = self.simulate_web_page(url)
            
        browser_text.insert(1.0, content)
        self.status_bar.config(text=f"Loaded: {url}")
        
    def get_home_page(self):
        """Get browser home page"""
        return f"""
        ================================================
                      PYTHON OS BROWSER
        ================================================
        
        Welcome to the Python OS Web Browser!
        
        Features:
        • Simulated web browsing
        • Tabbed interface
        • History and bookmarks
        • Internal pages
        
        Quick Links:
        • Python.org - The official Python website
        • Tkinter Docs - Documentation for Tkinter GUI
        • GitHub - Code hosting platform
        • Simulated News - Fake news articles
        
        This is a simulated browser for the Python OS.
        Real websites cannot be accessed, but you can
        try entering URLs to see simulated pages.
        
        Try entering:
        • python.org
        • github.com
        • news.example.com
        • about:settings
        
        ================================================
        """
        
    def get_news_page(self):
        """Get simulated news page"""
        import random
        news_items = [
            ("Python OS 2.0 Released", "The latest version of Python OS includes new features..."),
            ("Simulated Economy Booms", "Virtual markets reach all-time highs..."),
            ("AI Integration Planned", "Future versions to include AI assistants..."),
            ("Security Update Available", "Patch for simulated vulnerabilities released..."),
            ("Developer Conference", "Annual Python OS developer meetup announced...")
        ]
        
        content = "=" * 50 + "\n"
        content += "SIMULATED NEWS NETWORK\n"
        content += "=" * 50 + "\n\n"
        
        for title, description in random.sample(news_items, 3):
            content += f"📰 {title}\n"
            content += f"{description}\n\n"
            content += "-" * 50 + "\n\n"
            
        return content
        
    def simulate_web_page(self, url):
        """Simulate a web page based on URL"""
        domain = url.split('//')[-1].split('/')[0].lower()
        
        simulations = {
            'python.org': """
            ========================================
            WELCOME TO PYTHON.ORG (SIMULATED)
            ========================================
            
            Python is a programming language that lets you
            work quickly and integrate systems more effectively.
            
            Latest News:
            • Python 3.12 released!
            • PyCon 2024 announced
            • New packaging standards
            
            Downloads | Documentation | Community
            
            This is a simulated version of python.org
            for the Python OS browser.
            """,
            'github.com': """
            ========================================
            GITHUB (SIMULATED)
            ========================================
            
            Where the world builds software.
            
            Trending Repositories:
            1. python-os-simulator
            2. ai-framework
            3. quantum-computing-sim
            
            Explore | Marketplace | Pricing
            
            Sign up for free simulated account!
            """,
            'news.example.com': """
            ========================================
            EXAMPLE NEWS (SIMULATED)
            ========================================
            
            BREAKING: Python OS gains popularity!
            
            The simulated operating system built with Python
            and Tkinter has attracted virtual users worldwide.
            
            Features include:
            • Desktop environment
            • Web browser
            • Media player
            • File explorer
            
            This is a simulated news website.
            """
        }
        
        if domain in simulations:
            return simulations[domain]
        else:
            return f"""
            ========================================
            {domain.upper()} (SIMULATED)
            ========================================
            
            Welcome to {domain}!
            
            This is a simulated web page for the
            Python OS browser.
            
            The actual website cannot be accessed
            from this simulated browser.
            
            Try one of these instead:
            • python.org
            • github.com
            • news.example.com
            """
            
    def go_back(self):
        """Go to previous page in history"""
        if len(self.history) > 1:
            self.history.pop()  # Remove current
            previous = self.history.pop()  # Get previous
            self.load_page(previous)
            
    def go_forward(self):
        """Go forward in history (simplified)"""
        # In a real browser, you'd have forward history
        messagebox.showinfo("Forward", "Forward navigation not implemented in simulation")
        
    def refresh_page(self):
        """Refresh current page"""
        current_url = self.url_var.get()
        if current_url:
            self.load_page(current_url)
            
    def show_bookmarks(self):
        """Show bookmarks menu"""
        menu = tk.Menu(self.window, tearoff=0)
        for name, url in self.bookmarks:
            menu.add_command(
                label=name,
                command=lambda u=url: self.load_page(u)
            )
        menu.add_separator()
        menu.add_command(label="Add Bookmark", command=self.add_bookmark)
        menu.add_command(label="Manage Bookmarks", command=self.manage_bookmarks)
        
        menu.post(self.window.winfo_pointerx(), self.window.winfo_pointery())
        
    def add_bookmark(self):
        """Add current page to bookmarks"""
        url = self.url_var.get()
        name = simpledialog.askstring("Add Bookmark", "Bookmark name:")
        if name and url:
            self.bookmarks.append((name, url))
            messagebox.showinfo("Bookmark Added", f"Added '{name}' to bookmarks")
            
    def manage_bookmarks(self):
        """Manage bookmarks window"""
        # Implement bookmark management
        pass