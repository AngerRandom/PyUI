# themes/theme_manager.py - Enhanced with custom themes
import json
import os
from tkinter import font
import tkinter as tk

class ThemeManager:
    def __init__(self):
        self.themes = {}
        self.custom_themes = {}
        self.current_theme = 'default'
        self.load_themes()
        
    def load_themes(self):
        """Load built-in and custom themes"""
        # Built-in themes
        self.themes = {
            'default': {
                'name': 'Default',
                'background': '#2c3e50',
                'foreground': '#ecf0f1',
                'accent': '#3498db',
                'error': '#e74c3c',
                'success': '#2ecc71',
                'warning': '#f39c12',
                'info': '#9b59b6',
                'font_family': 'Segoe UI',
                'font_size': 11,
                'cursor': 'arrow',
                'button_bg': '#3498db',
                'button_fg': 'white',
                'entry_bg': '#34495e',
                'entry_fg': 'white',
                'taskbar_bg': '#1a1a1a',
                'taskbar_fg': 'white',
                'start_button_bg': '#0078d7',
                'start_button_fg': 'white',
                'menu_bg': '#2d2d30',
                'menu_fg': '#cccccc',
                'panel_bg': '#252526',
                'highlight': '#3e3e42',
                'wallpaper': 'assets/wallpaper/default.jpg'
            },
            'dark': {
                'name': 'Dark',
                'background': '#1e1e1e',
                'foreground': '#d4d4d4',
                'accent': '#007acc',
                'error': '#f44747',
                'success': '#4ec9b0',
                'warning': '#dcdcaa',
                'info': '#c586c0',
                'font_family': 'Consolas',
                'font_size': 11,
                'cursor': 'xterm',
                'button_bg': '#0e639c',
                'button_fg': 'white',
                'entry_bg': '#252526',
                'entry_fg': '#cccccc',
                'taskbar_bg': '#2d2d30',
                'taskbar_fg': '#cccccc',
                'start_button_bg': '#0078d7',
                'start_button_fg': 'white',
                'menu_bg': '#252526',
                'menu_fg': '#cccccc',
                'panel_bg': '#2d2d30',
                'highlight': '#3e3e42',
                'wallpaper': 'assets/wallpaper/dark.jpg'
            },
            'light': {
                'name': 'Light',
                'background': '#ffffff',
                'foreground': '#000000',
                'accent': '#007acc',
                'error': '#dc3545',
                'success': '#28a745',
                'warning': '#ffc107',
                'info': '#17a2b8',
                'font_family': 'Segoe UI',
                'font_size': 11,
                'cursor': 'arrow',
                'button_bg': '#007acc',
                'button_fg': 'white',
                'entry_bg': '#f8f9fa',
                'entry_fg': '#212529',
                'taskbar_bg': '#f8f9fa',
                'taskbar_fg': '#212529',
                'start_button_bg': '#0078d7',
                'start_button_fg': 'white',
                'menu_bg': '#ffffff',
                'menu_fg': '#212529',
                'panel_bg': '#f8f9fa',
                'highlight': '#e9ecef',
                'wallpaper': 'assets/wallpaper/light.jpg'
            },
            'blue': {
                'name': 'Blue',
                'background': '#1c2833',
                'foreground': '#d6dbdf',
                'accent': '#3498db',
                'error': '#e74c3c',
                'success': '#2ecc71',
                'warning': '#f1c40f',
                'info': '#9b59b6',
                'font_family': 'Arial',
                'font_size': 11,
                'cursor': 'arrow',
                'button_bg': '#2980b9',
                'button_fg': 'white',
                'entry_bg': '#2c3e50',
                'entry_fg': '#ecf0f1',
                'taskbar_bg': '#1b2631',
                'taskbar_fg': '#ecf0f1',
                'start_button_bg': '#3498db',
                'start_button_fg': 'white',
                'menu_bg': '#2c3e50',
                'menu_fg': '#ecf0f1',
                'panel_bg': '#34495e',
                'highlight': '#4a6572',
                'wallpaper': 'assets/wallpaper/blue.jpg'
            }
        }
        
        # Load custom themes
        self.load_custom_themes()
        
    def load_custom_themes(self):
        """Load custom themes from file"""
        theme_file = 'themes/custom_themes.json'
        if os.path.exists(theme_file):
            try:
                with open(theme_file, 'r') as f:
                    self.custom_themes = json.load(f)
            except Exception as e:
                print(f"Error loading custom themes: {e}")
                self.custom_themes = {}
        else:
            # Create example custom theme
            self.custom_themes = {
                'my_theme': {
                    'name': 'My Custom Theme',
                    'background': '#2d3436',
                    'foreground': '#dfe6e9',
                    'accent': '#00b894',
                    'error': '#d63031',
                    'success': '#00cec9',
                    'warning': '#fdcb6e',
                    'info': '#6c5ce7'
                }
            }
            self.save_custom_themes()
            
    def save_custom_themes(self):
        """Save custom themes to file"""
        os.makedirs('themes', exist_ok=True)
        with open('themes/custom_themes.json', 'w') as f:
            json.dump(self.custom_themes, f, indent=4)
            
    def get_current_theme(self):
        """Get current theme settings"""
        return self.get_theme(self.current_theme)
        
    def get_theme(self, theme_name):
        """Get theme settings by name"""
        # Check custom themes first
        if theme_name in self.custom_themes:
            # Merge with default theme for missing properties
            theme = self.themes['default'].copy()
            theme.update(self.custom_themes[theme_name])
            return theme
            
        if theme_name in self.themes:
            return self.themes[theme_name]
        else:
            return self.themes['default']
            
    def set_theme(self, theme_name):
        """Set current theme"""
        if theme_name in self.themes or theme_name in self.custom_themes:
            self.current_theme = theme_name
            return True
        return False
        
    def create_custom_theme(self, theme_name, theme_data):
        """Create a new custom theme"""
        self.custom_themes[theme_name] = theme_data
        self.save_custom_themes()
        return True
        
    def delete_custom_theme(self, theme_name):
        """Delete a custom theme"""
        if theme_name in self.custom_themes:
            del self.custom_themes[theme_name]
            self.save_custom_themes()
            return True
        return False
        
    def get_available_themes(self):
        """Get list of all available themes"""
        themes = {}
        themes.update({k: v['name'] for k, v in self.themes.items()})
        themes.update({k: v['name'] for k, v in self.custom_themes.items()})
        return themes
        
    def apply_theme_to_widget(self, widget, theme_name=None):
        """Apply theme to a widget and its children"""
        theme = self.get_theme(theme_name or self.current_theme)
        
        try:
            # Apply to widget itself
            widget_type = widget.winfo_class()
            
            if widget_type in ['TFrame', 'Frame', 'Labelframe']:
                widget.config(bg=theme['background'])
            elif widget_type in ['TLabel', 'Label']:
                widget.config(bg=theme['background'], fg=theme['foreground'])
            elif widget_type in ['TButton', 'Button']:
                widget.config(bg=theme['button_bg'], fg=theme['button_fg'])
            elif widget_type in ['TEntry', 'Entry']:
                widget.config(bg=theme['entry_bg'], fg=theme['entry_fg'],
                            insertbackground=theme['foreground'])
            elif widget_type in ['Text']:
                widget.config(bg=theme['entry_bg'], fg=theme['entry_fg'],
                            insertbackground=theme['foreground'])
            elif widget_type in ['Listbox']:
                widget.config(bg=theme['entry_bg'], fg=theme['entry_fg'])
                
        except Exception as e:
            pass
            
        # Apply to children
        for child in widget.winfo_children():
            self.apply_theme_to_widget(child, theme_name)
