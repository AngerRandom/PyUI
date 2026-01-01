import tkinter as tk
from tkinter import scrolledtext
import os
import subprocess
import platform

class TerminalApp:
    def __init__(self, parent, os_app):
        self.os_app = os_app
        self.parent = parent
        
        # Create terminal window
        self.window = tk.Toplevel(parent)
        self.window.title("Terminal")
        self.window.geometry("800x500")
        
        # Set theme
        self.bg_color = '#1e1e1e'
        self.fg_color = '#ffffff'
        self.prompt_color = '#4caf50'
        
        # Create terminal UI
        self.setup_ui()
        
        # Initial prompt
        self.insert_prompt()
        
        # Bind events
        self.text_area.bind('<Return>', self.process_command)
        self.text_area.bind('<Key>', self.on_key_press)
        
        # History
        self.command_history = []
        self.history_index = -1
        
    def setup_ui(self):
        """Setup terminal UI"""
        # Text area
        self.text_area = scrolledtext.ScrolledText(
            self.window,
            wrap=tk.WORD,
            bg=self.bg_color,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            font=('Courier New', 11)
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # Set focus
        self.text_area.focus_set()
        
    def insert_prompt(self):
        """Insert command prompt"""
        prompt = f"\n{self.os_app.current_user}@simulator:~$ "
        self.text_area.insert(tk.END, prompt, 'prompt')
        self.text_area.tag_config('prompt', foreground=self.prompt_color)
        self.text_area.mark_set(tk.INSERT, tk.END)
        self.text_area.see(tk.END)
        
    def on_key_press(self, event):
        """Handle key presses"""
        # Handle up/down arrows for history
        if event.keysym == 'Up':
            if self.command_history:
                if self.history_index < len(self.command_history) - 1:
                    self.history_index += 1
                self.show_history_command()
            return 'break'
        elif event.keysym == 'Down':
            if self.history_index > 0:
                self.history_index -= 1
                self.show_history_command()
            elif self.history_index == 0:
                self.history_index = -1
                self.clear_command_line()
            return 'break'
            
        # Prevent editing prompt
        cursor_pos = self.text_area.index(tk.INSERT)
        last_prompt_pos = self.text_area.search(
            '~$', 
            'end-1c', 
            backwards=True, 
            regexp=False
        )
        
        if last_prompt_pos:
            last_prompt_line = int(last_prompt_pos.split('.')[0])
            current_line = int(cursor_pos.split('.')[0])
            
            if current_line < last_prompt_line:
                return 'break'
            elif current_line == last_prompt_line:
                prompt_end = f"{last_prompt_line}.{int(last_prompt_pos.split('.')[1]) + 2}"
                if self.text_area.compare(cursor_pos, '<', prompt_end):
                    return 'break'
                    
    def show_history_command(self):
        """Show command from history"""
        if self.history_index >= 0:
            self.clear_command_line()
            command = self.command_history[self.history_index]
            self.text_area.insert(tk.END, command)
            
    def clear_command_line(self):
        """Clear current command line"""
        last_prompt_pos = self.text_area.search(
            '~$', 
            'end-1c', 
            backwards=True, 
            regexp=False
        )
        if last_prompt_pos:
            prompt_end = f"{last_prompt_pos}+2c"
            self.text_area.delete(prompt_end, tk.END)
            
    def process_command(self, event=None):
        """Process entered command"""
        # Get command
        last_prompt_pos = self.text_area.search(
            '~$', 
            'end-1c', 
            backwards=True, 
            regexp=False
        )
        
        if last_prompt_pos:
            prompt_end = f"{last_prompt_pos}+2c"
            command = self.text_area.get(prompt_end, 'end-1c').strip()
            
            # Add to history
            if command and (not self.command_history or self.command_history[0] != command):
                self.command_history.insert(0, command)
                self.history_index = -1
                
            # Execute command
            self.execute_command(command)
            
        self.insert_prompt()
        return 'break'
        
    def execute_command(self, command):
        """Execute terminal command"""
        if not command:
            return
            
        # Handle setup command
        elif command == 'setup':
            self.text_area.insert(tk.END, "\nLaunching setup wizard...")
            self.os_app.show_setup_wizard()
            
        # Handle reset-setup command
        elif command == 'reset-setup':
            self.text_area.insert(tk.END, "\nResetting setup configuration...")
            self.os_app.db.set_system_info('setup_completed', 'false')
            self.text_area.insert(tk.END, "\nSetup has been reset. Restart to run setup wizard.")
            
            
        # Handle help
        elif command == 'help':
            help_text = """
Available commands:
- help: Show this help
- clear: Clear terminal
- echo [text]: Print text
- ls [dir]: List directory
- pwd: Print working directory
- date: Show date and time
- whoami: Show current user
- theme [name]: Change theme
- shutdown: Shutdown system
- reboot: Reboot system
"""
            self.text_area.insert(tk.END, f"\n{help_text}")
            
        # Handle clear
        elif command == 'clear':
            self.text_area.delete(1.0, tk.END)
            self.insert_prompt()
            
        # Handle echo
        elif command.startswith('echo '):
            text = command[5:]
            self.text_area.insert(tk.END, f"\n{text}")
            
        # Handle ls
        elif command.startswith('ls'):
            path = command[3:] if len(command) > 2 else '/home/admin'
            try:
                files = self.os_app.db.list_directory(path)
                if files:
                    for name, ftype, size, modified in files:
                        self.text_area.insert(tk.END, f"\n{ftype[0]} {name:20} {size:8}")
                else:
                    self.text_area.insert(tk.END, f"\nDirectory '{path}' is empty")
            except Exception as e:
                self.text_area.insert(tk.END, f"\nError: {e}")
                
        # Handle pwd
        elif command == 'pwd':
            self.text_area.insert(tk.END, f"\n/home/admin")
            
        # Handle date
        elif command == 'date':
            from datetime import datetime
            self.text_area.insert(tk.END, f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        # Handle whoami
        elif command == 'whoami':
            self.text_area.insert(tk.END, f"\n{self.os_app.current_user}")
            
        # Handle theme
        elif command.startswith('theme '):
            theme_name = command[6:]
            self.text_area.insert(tk.END, f"\nChanging theme to {theme_name}...")
            # In a full implementation, you would change the theme
            
        # Handle shutdown
        elif command == 'shutdown':
            self.os_app.show_shutdown_screen()
            
        # Handle reboot
        elif command == 'reboot':
            self.text_area.insert(tk.END, "\nRebooting system...")
            self.window.after(2000, lambda: self.os_app.show_boot_screen())
            
        # Unknown command
        else:
            self.text_area.insert(tk.END, f"\nCommand not found: {command}")
