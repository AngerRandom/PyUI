# window_manager.py
import tkinter as tk
from tkinter import ttk
import time

class WindowManager:
    def __init__(self):
        self.windows = {}
        self.window_order = []
        self.active_window = None
        
    def register_window(self, name, window):
        """Register a window with the window manager"""
        self.windows[name] = {
            'window': window,
            'title': window.title() if hasattr(window, 'title') else name,
            'state': 'normal',
            'z_index': len(self.windows),
            'minimized': False,
            'position': None
        }
        self.window_order.append(name)
        
        # Configure window
        if isinstance(window, tk.Toplevel):
            window.protocol("WM_DELETE_WINDOW", lambda: self.close_window(name))
            
        self.update_taskbar()
        
    def close_window(self, name):
        """Close a window"""
        if name in self.windows:
            window_info = self.windows[name]
            window_info['window'].destroy()
            del self.windows[name]
            self.window_order.remove(name)
            self.update_taskbar()
            
    def minimize_window(self, name):
        """Minimize a window"""
        if name in self.windows:
            window_info = self.windows[name]
            if isinstance(window_info['window'], tk.Toplevel):
                window_info['window'].withdraw()
                window_info['minimized'] = True
                window_info['state'] = 'withdrawn'
                self.update_taskbar()
                
    def restore_window(self, name):
        """Restore a minimized window"""
        if name in self.windows:
            window_info = self.windows[name]
            if isinstance(window_info['window'], tk.Toplevel):
                window_info['window'].deiconify()
                window_info['minimized'] = False
                window_info['state'] = 'normal'
                self.bring_to_front(name)
                self.update_taskbar()
                
    def bring_to_front(self, name):
        """Bring window to front"""
        if name in self.windows:
            window_info = self.windows[name]
            if isinstance(window_info['window'], tk.Toplevel):
                window_info['window'].lift()
                window_info['window'].focus_force()
                
            # Update z-index
            if name in self.window_order:
                self.window_order.remove(name)
                self.window_order.append(name)
                
            self.active_window = name
            
    def cascade_windows(self):
        """Arrange windows in cascade"""
        x_offset = 30
        y_offset = 30
        screen_width = 1024
        screen_height = 768
        
        for i, name in enumerate(self.window_order):
            if name in self.windows:
                window_info = self.windows[name]
                window = window_info['window']
                
                if isinstance(window, tk.Toplevel):
                    x = x_offset * (i % 5)
                    y = y_offset * (i % 5)
                    
                    if x + window.winfo_width() > screen_width:
                        x = screen_width - window.winfo_width() - 50
                    if y + window.winfo_height() > screen_height:
                        y = screen_height - window.winfo_height() - 50
                        
                    window.geometry(f"+{x}+{y}")
                    
    def tile_windows(self):
        """Arrange windows in tile pattern"""
        if not self.windows:
            return
            
        screen_width = 1024
        screen_height = 700  # Leave space for taskbar
        
        window_count = len([w for w in self.windows.values() if not w['minimized']])
        if window_count == 0:
            return
            
        import math
        cols = math.ceil(math.sqrt(window_count))
        rows = math.ceil(window_count / cols)
        
        window_width = screen_width // cols
        window_height = screen_height // rows
        
        visible_windows = [name for name in self.window_order 
                          if name in self.windows and not self.windows[name]['minimized']]
        
        for i, name in enumerate(visible_windows):
            window_info = self.windows[name]
            window = window_info['window']
            
            if isinstance(window, tk.Toplevel):
                col = i % cols
                row = i // cols
                
                x = col * window_width
                y = row * window_height
                
                window.geometry(f"{window_width}x{window_height}+{x}+{y}")
                
    def update_taskbar(self):
        """Update taskbar with current windows"""
        # This would be called by the desktop to update taskbar buttons
        pass
        
    def get_window_list(self):
        """Get list of all windows"""
        return [{
            'name': name,
            'title': info['title'],
            'state': info['state'],
            'minimized': info['minimized']
        } for name, info in self.windows.items()]