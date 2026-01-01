# applications/package_manager.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import importlib.util
import sys

class PackageManagerApp:
    def __init__(self, parent, os_app):
        self.os_app = os_app
        self.parent = parent
        
        # Available packages (simulated repository)
        self.available_packages = self.load_package_repository()
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Package Manager")
        self.window.geometry("800x600")
        
        self.setup_ui()
        
    def load_package_repository(self):
        """Load available packages from repository"""
        return {
            'calculator': {
                'name': 'Calculator',
                'version': '1.0',
                'author': 'Python OS Team',
                'description': 'Scientific calculator with graphing',
                'category': 'Utilities',
                'size': '2.4 MB',
                'dependencies': []
            },
            'text-editor': {
                'name': 'Advanced Text Editor',
                'version': '2.0',
                'author': 'Code Masters',
                'description': 'Feature-rich text editor with syntax highlighting',
                'category': 'Development',
                'size': '5.1 MB',
                'dependencies': ['python>=3.8']
            },
            'calendar': {
                'name': 'Calendar',
                'version': '1.2',
                'author': 'Productivity Inc',
                'description': 'Desktop calendar with reminders',
                'category': 'Productivity',
                'size': '3.2 MB',
                'dependencies': []
            },
            'photo-viewer': {
                'name': 'Photo Viewer',
                'version': '1.5',
                'author': 'Media Tools',
                'description': 'Image viewer with editing capabilities',
                'category': 'Graphics',
                'size': '4.7 MB',
                'dependencies': ['pillow']
            },
            'notes-app': {
                'name': 'Notes',
                'version': '1.1',
                'author': 'Python OS Team',
                'description': 'Simple note-taking application',
                'category': 'Productivity',
                'size': '1.8 MB',
                'dependencies': []
            }
        }
        
    def setup_ui(self):
        """Setup package manager UI"""
        # Main container
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Toolbar
        toolbar = tk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(
            toolbar,
            text="Refresh",
            command=self.refresh_packages
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            toolbar,
            text="Install Selected",
            bg='#4CAF50',
            fg='white',
            command=self.install_selected
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            toolbar,
            text="Uninstall Selected",
            bg='#f44336',
            fg='white',
            command=self.uninstall_selected
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            toolbar,
            text="Update All",
            bg='#2196F3',
            fg='white',
            command=self.update_all
        ).pack(side=tk.LEFT, padx=2)
        
        # Search
        search_frame = tk.Frame(toolbar)
        search_frame.pack(side=tk.RIGHT)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_packages)
        tk.Entry(search_frame, textvariable=self.search_var, width=20).pack(side=tk.LEFT, padx=5)
        
        # Notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Available packages tab
        available_frame = tk.Frame(notebook)
        notebook.add(available_frame, text="Available Packages")
        
        self.setup_available_tab(available_frame)
        
        # Installed packages tab
        installed_frame = tk.Frame(notebook)
        notebook.add(installed_frame, text="Installed Packages")
        
        self.setup_installed_tab(installed_frame)
        
        # Updates tab
        updates_frame = tk.Frame(notebook)
        notebook.add(updates_frame, text="Updates")
        
        self.setup_updates_tab(updates_frame)
        
        # Status bar
        self.status_bar = tk.Label(
            self.window,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_available_tab(self, parent):
        """Setup available packages tab"""
        # Treeview for packages
        columns = ('name', 'version', 'category', 'size', 'description')
        self.available_tree = ttk.Treeview(
            parent,
            columns=columns,
            show='headings',
            selectmode='extended'
        )
        
        # Define headings
        self.available_tree.heading('name', text='Package')
        self.available_tree.heading('version', text='Version')
        self.available_tree.heading('category', text='Category')
        self.available_tree.heading('size', text='Size')
        self.available_tree.heading('description', text='Description')
        
        # Define columns
        self.available_tree.column('name', width=150)
        self.available_tree.column('version', width=80)
        self.available_tree.column('category', width=100)
        self.available_tree.column('size', width=80)
        self.available_tree.column('description', width=300)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.available_tree.yview)
        self.available_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.available_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate packages
        self.populate_available_packages()
        
        # Double-click to view details
        self.available_tree.bind('<Double-1>', self.show_package_details)
        
    def populate_available_packages(self):
        """Populate available packages list"""
        for item in self.available_tree.get_children():
            self.available_tree.delete(item)
            
        for pkg_id, pkg_info in self.available_packages.items():
            self.available_tree.insert('', tk.END, iid=pkg_id,
                values=(pkg_info['name'], pkg_info['version'], 
                       pkg_info['category'], pkg_info['size'],
                       pkg_info['description']))
                       
    def setup_installed_tab(self, parent):
        """Setup installed packages tab"""
        columns = ('name', 'version', 'author', 'installed_date')
        self.installed_tree = ttk.Treeview(
            parent,
            columns=columns,
            show='headings',
            selectmode='extended'
        )
        
        self.installed_tree.heading('name', text='Package')
        self.installed_tree.heading('version', text='Version')
        self.installed_tree.heading('author', text='Author')
        self.installed_tree.heading('installed_date', text='Installed')
        
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.installed_tree.yview)
        self.installed_tree.configure(yscrollcommand=scrollbar.set)
        
        self.installed_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.populate_installed_packages()
        
    def populate_installed_packages(self):
        """Populate installed packages list"""
        for item in self.installed_tree.get_children():
            self.installed_tree.delete(item)
            
        # Get installed apps from database
        self.os_app.db.connect()
        self.os_app.db.cursor.execute('''
            SELECT name, version, author, installed_at 
            FROM installed_apps 
            WHERE is_system_app = 0
            ORDER BY name
        ''')
        
        for row in self.os_app.db.cursor.fetchall():
            self.installed_tree.insert('', tk.END,
                values=(row[0], row[1], row[2], row[3]))
                
    def setup_updates_tab(self, parent):
        """Setup updates tab"""
        update_frame = tk.Frame(parent)
        update_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            update_frame,
            text="Available Updates",
            font=('Arial', 14, 'bold')
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Updates listbox
        self.updates_listbox = tk.Listbox(update_frame, height=10)
        self.updates_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Check for updates button
        tk.Button(
            update_frame,
            text="Check for Updates",
            command=self.check_for_updates
        ).pack(pady=5)
        
        tk.Button(
            update_frame,
            text="Install All Updates",
            bg='#4CAF50',
            fg='white'
        ).pack(pady=5)
        
    def install_selected(self):
        """Install selected packages"""
        selected = self.available_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select packages to install")
            return
            
        for pkg_id in selected:
            self.install_package(pkg_id)
            
    def install_package(self, pkg_id):
        """Install a package"""
        if pkg_id not in self.available_packages:
            messagebox.showerror("Error", f"Package '{pkg_id}' not found")
            return
            
        pkg_info = self.available_packages[pkg_id]
        
        # Check dependencies
        if pkg_info.get('dependencies'):
            if not self.check_dependencies(pkg_info['dependencies']):
                if not messagebox.askyesno("Dependencies", 
                      f"Missing dependencies: {', '.join(pkg_info['dependencies'])}\n"
                      "Continue anyway?"):
                    return
                    
        # Simulate installation
        self.status_bar.config(text=f"Installing {pkg_info['name']}...")
        self.window.update()
        
        # Add to database
        self.os_app.db.connect()
        self.os_app.db.cursor.execute('''
            INSERT OR REPLACE INTO installed_apps 
            (name, version, author, description, entry_point, category, is_system_app)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            pkg_info['name'],
            pkg_info['version'],
            pkg_info['author'],
            pkg_info['description'],
            f'applications.{pkg_id}.{pkg_info["name"].replace(" ", "")}',
            pkg_info['category'],
            0
        ))
        self.os_app.db.connection.commit()
        
        # Create stub application file
        self.create_stub_application(pkg_id, pkg_info)
        
        # Update installed packages list
        self.populate_installed_packages()
        
        # Update OS app list
        self.os_app.installed_apps = self.os_app.load_installed_apps()
        
        self.status_bar.config(text=f"Successfully installed {pkg_info['name']}")
        messagebox.showinfo("Installation Complete", 
                          f"{pkg_info['name']} has been installed successfully!")
                          
    def create_stub_application(self, pkg_id, pkg_info):
        """Create a stub application file for the package"""
        app_dir = 'applications'
        os.makedirs(app_dir, exist_ok=True)
        
        app_file = os.path.join(app_dir, f"{pkg_id}.py")
        
        stub_code = f'''# Auto-generated application stub for {pkg_info['name']}
import tkinter as tk
from tkinter import messagebox

class {pkg_info['name'].replace(' ', '')}:
    def __init__(self, parent, os_app):
        self.os_app = os_app
        self.parent = parent
        
        self.window = tk.Toplevel(parent)
        self.window.title("{pkg_info['name']}")
        self.window.geometry("400x300")
        
        # Application content
        tk.Label(
            self.window,
            text="{pkg_info['name']} v{pkg_info['version']}",
            font=('Arial', 16, 'bold')
        ).pack(pady=20)
        
        tk.Label(
            self.window,
            text="This application was installed via Package Manager",
            wraplength=350
        ).pack(pady=10)
        
        tk.Label(
            self.window,
            text="Author: {pkg_info['author']}",
            font=('Arial', 10)
        ).pack(pady=5)
        
        tk.Label(
            self.window,
            text="{pkg_info['description']}",
            wraplength=350
        ).pack(pady=20)
        
        # Close button
        tk.Button(
            self.window,
            text="Close",
            command=self.window.destroy
        ).pack(pady=20)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = {pkg_info['name'].replace(' ', '')}(root, None)
    root.mainloop()
'''
        
        with open(app_file, 'w') as f:
            f.write(stub_code)
            
    def check_dependencies(self, dependencies):
        """Check if dependencies are satisfied"""
        # Simplified dependency check
        return True
        
    def uninstall_selected(self):
        """Uninstall selected packages"""
        selected = self.installed_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select packages to uninstall")
            return
            
        for item in selected:
            values = self.installed_tree.item(item)['values']
            if values:
                package_name = values[0]
                self.uninstall_package(package_name)
                
    def uninstall_package(self, package_name):
        """Uninstall a package"""
        if messagebox.askyesno("Confirm Uninstall", 
                             f"Are you sure you want to uninstall {package_name}?"):
            
            # Remove from database
            self.os_app.db.connect()
            self.os_app.db.cursor.execute('''
                DELETE FROM installed_apps WHERE name = ?
            ''', (package_name,))
            self.os_app.db.connection.commit()
            
            # Update lists
            self.populate_installed_packages()
            self.os_app.installed_apps = self.os_app.load_installed_apps()
            
            self.status_bar.config(text=f"Uninstalled {package_name}")
            
    def update_all(self):
        """Update all packages"""
        messagebox.showinfo("Update", "Checking for updates...")
        
    def check_for_updates(self):
        """Check for available updates"""
        self.updates_listbox.delete(0, tk.END)
        self.updates_listbox.insert(tk.END, "No updates available at this time.")
        self.updates_listbox.insert(tk.END, "All packages are up to date.")
        
    def filter_packages(self, *args):
        """Filter packages based on search term"""
        search_term = self.search_var.get().lower()
        
        for item in self.available_tree.get_children():
            values = self.available_tree.item(item)['values']
            if values:
                # Check if search term matches any field
                matches = any(search_term in str(value).lower() for value in values)
                self.available_tree.item(item, tags=('visible' if matches else 'hidden'))
                
        # Configure tag to hide items
        self.available_tree.tag_configure('hidden', foreground='gray')
        
    def show_package_details(self, event):
        """Show details for selected package"""
        selection = self.available_tree.selection()
        if selection:
            pkg_id = selection[0]
            pkg_info = self.available_packages.get(pkg_id)
            
            if pkg_info:
                self.show_details_window(pkg_id, pkg_info)
                
    def show_details_window(self, pkg_id, pkg_info):
        """Show package details window"""
        details_win = tk.Toplevel(self.window)
        details_win.title(f"Package Details: {pkg_info['name']}")
        details_win.geometry("500x400")
        
        # Details content
        content = f"""
        Package: {pkg_info['name']}
        Version: {pkg_info['version']}
        Author: {pkg_info['author']}
        Category: {pkg_info['category']}
        Size: {pkg_info['size']}
        
        Description:
        {pkg_info['description']}
        
        Dependencies: {', '.join(pkg_info.get('dependencies', ['None']))}
        
        Package ID: {pkg_id}
        """
        
        text_widget = scrolledtext.ScrolledText(details_win, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(1.0, content)
        text_widget.config(state=tk.DISABLED)
        
        # Install button
        tk.Button(
            details_win,
            text="Install",
            bg='#4CAF50',
            fg='white',
            command=lambda: self.install_package(pkg_id)
        ).pack(pady=10)