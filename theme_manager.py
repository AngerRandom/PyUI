import json
import os
from tkinter import font

class ThemeManager:
    def __init__(self):
        self.themes = {}
        self.current_theme = 'default'
        self.load_themes()
        
    def load_themes(self):
        """Load themes from file"""
        default_themes = {
            'default': {
                'name': 'Default',
                'background': '#2c3e50',
                'foreground': '#ecf0f1',
                'accent': '#3498db',
                'error': '#e74c3c',
                'success': '#2ecc71',
                'warning': '#f39c12',
                'font_family': 'Arial',
                'font_size': 11,
                'cursor': 'arrow',
                'button_bg': '#3498db',
                'button_fg': 'white',
                'entry_bg': '#34495e',
                'entry_fg': 'white'
            },
            'dark': {
                'name': 'Dark',
                'background': '#1a1a1a',
                'foreground': '#ffffff',
                'accent': '#007acc',
                'error': '#f44747',
                'success': '#4ec9b0',
                'warning': '#dcdcaa',
                'font_family': 'Consolas',
                'font_size': 11,
                'cursor': 'xterm',
                'button_bg': '#0e639c',
                'button_fg': 'white',
                'entry_bg': '#252526',
                'entry_fg': '#cccccc'
            },
            'light': {
                'name': 'Light',
                'background': '#ffffff',
                'foreground': '#000000',
                'accent': '#007acc',
                'error': '#dc3545',
                'success': '#28a745',
                'warning': '#ffc107',
                'font_family': 'Segoe UI',
                'font_size': 11,
                'cursor': 'arrow',
                'button_bg': '#007acc',
                'button_fg': 'white',
                'entry_bg': '#f8f9fa',
                'entry_fg': '#212529'
            }
        }
        
        # Try to load from file
        theme_file = 'themes/themes.json'
        if os.path.exists(theme_file):
            try:
                with open(theme_file, 'r') as f:
                    self.themes = json.load(f)
            except Exception as e:
                print(f"Error loading themes: {e}")
                self.themes = default_themes
        else:
            self.themes = default_themes
            # Save default themes
            os.makedirs('themes', exist_ok=True)
            with open(theme_file, 'w') as f:
                json.dump(default_themes, f, indent=4)
                
    def get_theme(self, theme_name=None):
        """Get theme settings"""
        if theme_name is None:
            theme_name = self.current_theme
            
        if theme_name in self.themes:
            return self.themes[theme_name]
        else:
            return self.themes['default']
            
    def set_theme(self, theme_name):
        """Set current theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            return True
        return False
        
    def apply_theme(self, widget, theme_name=None):
        """Apply theme to widget"""
        theme = self.get_theme(theme_name)
        
        # This is a simplified version - in a full implementation,
        # you would recursively apply the theme to all widgets
        try:
            widget.config(bg=theme['background'])
        except:
            pass