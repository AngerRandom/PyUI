# applications/trash_bin.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class TrashBin:
    def __init__(self, parent, os_app):
        self.os_app = os_app
        self.parent = parent
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Trash Bin")
        self.window.geometry("700x500")
        
        self.setup_ui()
        self.load_trash_items()
        
    def setup_ui(self):
        """Setup trash bin UI"""
        # Header
        header_frame = tk.Frame(self.window, bg='#3498db', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🗑️ Trash Bin",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#3498db'
        ).pack(pady=15)
        
        # Toolbar
        toolbar = tk.Frame(self.window)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        # Action buttons
        tk.Button(
            toolbar,
            text="Restore Selected",
            bg='#2ecc71',
            fg='white',
            command=self.restore_selected
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            toolbar,
            text="Delete Permanently",
            bg='#e74c3c',
            fg='white',
            command=self.delete_permanently
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            toolbar,
            text="Empty Trash",
            bg='#34495e',
            fg='white',
            command=self.empty_trash
        ).pack(side=tk.LEFT, padx=2)
        
        # Refresh button
        tk.Button(
            toolbar,
            text="↻ Refresh",
            command=self.load_trash_items
        ).pack(side=tk.RIGHT, padx=2)
        
        # Search
        search_frame = tk.Frame(toolbar)
        search_frame.pack(side=tk.RIGHT, padx=10)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_items)
        tk.Entry(search_frame, textvariable=self.search_var, width=20).pack(side=tk.LEFT, padx=5)
        
        # Main area - list of trash items
        list_frame = tk.Frame(self.window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview with columns
        columns = ('name', 'type', 'original_path', 'size', 'deleted_by', 'deleted_at', 'expires')
        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show='headings',
            selectmode='extended'
        )
        
        # Define columns
        column_configs = [
            ('name', 'Name', 150),
            ('type', 'Type', 80),
            ('original_path', 'Original Location', 200),
            ('size', 'Size', 80),
            ('deleted_by', 'Deleted By', 100),
            ('deleted_at', 'Deleted Date', 150),
            ('expires', 'Expires', 150)
        ]
        
        for col_id, heading, width in column_configs:
            self.tree.heading(col_id, text=heading)
            self.tree.column(col_id, width=width)
            
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar
        self.status_bar = tk.Label(
            self.window,
            text="",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind double-click to restore
        self.tree.bind('<Double-1>', lambda e: self.restore_selected())
        
        # Update status
        self.update_status()
        
    def load_trash_items(self):
        """Load trash items from database"""
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Get trash items
        items = self.os_app.db.get_trash_items(self.os_app.current_user)
        
        # Add to tree
        for item in items:
            size = self.format_size(item['size']) if item['size'] else '0 B'
            deleted_at = self.format_date(item['deleted_at'])
            expires_at = self.format_date(item['expires_at'])
            
            self.tree.insert('', 'end',
                values=(
                    item['name'],
                    item['type'],
                    item['original_path'],
                    size,
                    item['deleted_by'],
                    deleted_at,
                    expires_at
                ),
                tags=(item['id'],)
            )
            
        # Update status
        self.update_status()
        
    def format_size(self, size):
        """Format file size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
        
    def format_date(self, date_str):
        """Format date string"""
        if not date_str:
            return 'Unknown'
            
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M')
        except:
            return date_str[:16]
            
    def filter_items(self, *args):
        """Filter trash items based on search"""
        search_term = self.search_var.get().lower()
        
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            if values:
                # Check if search term matches any field
                matches = any(
                    search_term in str(value).lower() 
                    for value in values[:4]  # Search in name, type, path, size
                )
                
                if search_term and not matches:
                    self.tree.detach(item)
                else:
                    self.tree.reattach(item, '', 'end')
                    
    def get_selected_ids(self):
        """Get database IDs of selected items"""
        selected = self.tree.selection()
        ids = []
        
        for item in selected:
            tags = self.tree.item(item, 'tags')
            if tags:
                ids.append(int(tags[0]))
                
        return ids
        
    def restore_selected(self):
        """Restore selected items"""
        selected_ids = self.get_selected_ids()
        if not selected_ids:
            messagebox.showwarning("No Selection", "Please select items to restore.")
            return
            
        confirm = messagebox.askyesno(
            "Restore Items",
            f"Restore {len(selected_ids)} item(s) to their original locations?"
        )
        
        if not confirm:
            return
            
        restored_count = 0
        renamed_items = []
        
        for trash_id in selected_ids:
            success, new_name = self.os_app.db.restore_from_trash(trash_id)
            if success:
                restored_count += 1
                if new_name:
                    item = self.tree.item(self.tree.selection()[0])
                    original_name = item['values'][0]
                    renamed_items.append(f"{original_name} → {new_name}")
                    
        # Refresh list
        self.load_trash_items()
        
        # Show result
        message = f"Restored {restored_count} item(s)."
        if renamed_items:
            message += "\n\nSome items were renamed due to conflicts:\n"
            for rename in renamed_items:
                message += f"  • {rename}\n"
                
        messagebox.showinfo("Restore Complete", message)
        
    def delete_permanently(self):
        """Permanently delete selected items"""
        selected_ids = self.get_selected_ids()
        if not selected_ids:
            messagebox.showwarning("No Selection", "Please select items to delete.")
            return
            
        confirm = messagebox.askyesno(
            "Permanent Delete",
            f"Permanently delete {len(selected_ids)} item(s)?\n\n"
            "This action cannot be undone!"
        )
        
        if not confirm:
            return
            
        try:
            # Delete from trash table
            placeholders = ','.join('?' * len(selected_ids))
            self.os_app.db.cursor.execute(
                f'DELETE FROM trash WHERE id IN ({placeholders})',
                selected_ids
            )
            
            deleted_count = self.os_app.db.cursor.rowcount
            self.os_app.db.connection.commit()
            
            # Refresh list
            self.load_trash_items()
            
            messagebox.showinfo(
                "Delete Complete",
                f"Permanently deleted {deleted_count} item(s)."
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Cannot delete items: {e}")
            
    def empty_trash(self):
        """Empty the entire trash bin"""
        trash_size = self.os_app.db.get_trash_size(self.os_app.current_user)
        trash_count = len(self.tree.get_children())
        
        if trash_count == 0:
            messagebox.showinfo("Empty Trash", "Trash is already empty.")
            return
            
        confirm = messagebox.askyesno(
            "Empty Trash",
            f"Permanently delete all {trash_count} item(s) from trash?\n"
            f"Total size: {self.format_size(trash_size)}\n\n"
            "This action cannot be undone!"
        )
        
        if not confirm:
            return
            
        try:
            deleted_count = self.os_app.db.empty_trash(self.os_app.current_user)
            
            # Refresh list
            self.load_trash_items()
            
            messagebox.showinfo(
                "Trash Emptied",
                f"Emptied {deleted_count} item(s) from trash."
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Cannot empty trash: {e}")
            
    def update_status(self):
        """Update status bar with trash info"""
        trash_count = len(self.tree.get_children())
        trash_size = self.os_app.db.get_trash_size(self.os_app.current_user)
        
        self.status_bar.config(
            text=f"Items: {trash_count} | "
                 f"Total size: {self.format_size(trash_size)} | "
                 f"User: {self.os_app.current_user}"
        )