# applications/mobile_phone.py
import tkinter as tk
from tkinter import ttk, messagebox
import time
import random

class MobilePhone:
    def __init__(self, parent, os_app):
        self.os_app = os_app
        self.parent = parent
        
        # Create phone window
        self.window = tk.Toplevel(parent)
        self.window.title("Phone")
        self.window.geometry("360x600")
        
        self.setup_phone()
        
    def setup_phone(self):
        """Setup phone interface"""
        # Header
        header_frame = tk.Frame(self.window, bg='#4CAF50', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="Phone",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#4CAF50'
        ).pack(pady=15)
        
        # Tabs
        tab_frame = tk.Frame(self.window, bg='#f5f5f5')
        tab_frame.pack(fill=tk.X)
        
        tabs = ["Keypad", "Recents", "Contacts", "Voicemail"]
        self.tab_vars = {}
        
        for tab in tabs:
            btn = tk.Button(
                tab_frame,
                text=tab,
                font=('Arial', 12),
                bg='#f5f5f5',
                fg='#333333',
                relief=tk.FLAT,
                command=lambda t=tab: self.switch_tab(t)
            )
            btn.pack(side=tk.LEFT, expand=True, fill=tk.X, ipady=10)
            self.tab_vars[tab] = btn
            
        # Content area
        self.content_frame = tk.Frame(self.window, bg='white')
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Show keypad by default
        self.show_keypad()
        
    def show_keypad(self):
        """Show phone keypad"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Phone number display
        self.number_var = tk.StringVar()
        number_display = tk.Entry(
            self.content_frame,
            textvariable=self.number_var,
            font=('Arial', 24),
            justify=tk.CENTER,
            bg='white',
            fg='black',
            borderwidth=0,
            readonlybackground='white'
        )
        number_display.config(state='readonly')
        number_display.pack(fill=tk.X, pady=20, padx=20)
        
        # Keypad grid
        keypad_frame = tk.Frame(self.content_frame, bg='white')
        keypad_frame.pack(expand=True)
        
        # Keypad layout
        keys = [
            ('1', ''), ('2', 'ABC'), ('3', 'DEF'),
            ('4', 'GHI'), ('5', 'JKL'), ('6', 'MNO'),
            ('7', 'PQRS'), ('8', 'TUV'), ('9', 'WXYZ'),
            ('*', ''), ('0', '+'), ('#', '')
        ]
        
        for i, (main, sub) in enumerate(keys):
            row = i // 3
            col = i % 3
            
            key_btn = tk.Frame(keypad_frame, bg='#f0f0f0', relief=tk.RAISED, borderwidth=1)
            key_btn.grid(row=row, column=col, padx=5, pady=5, ipadx=20, ipady=20)
            
            # Main number
            main_label = tk.Label(
                key_btn,
                text=main,
                font=('Arial', 24, 'bold'),
                bg='#f0f0f0',
                fg='black'
            )
            main_label.pack()
            
            # Sub letters
            if sub:
                sub_label = tk.Label(
                    key_btn,
                    text=sub,
                    font=('Arial', 8),
                    bg='#f0f0f0',
                    fg='#666666'
                )
                sub_label.pack()
                
            # Bind click
            key_btn.bind('<Button-1>', lambda e, m=main: self.add_digit(m))
            main_label.bind('<Button-1>', lambda e, m=main: self.add_digit(m))
            if sub:
                sub_label.bind('<Button-1>', lambda e, m=main: self.add_digit(m))
                
        # Call buttons
        button_frame = tk.Frame(self.content_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=20)
        
        # Delete button
        delete_btn = tk.Button(
            button_frame,
            text="⌫",
            font=('Arial', 20),
            bg='#ff9800',
            fg='white',
            width=5,
            command=self.delete_digit
        )
        delete_btn.pack(side=tk.LEFT, padx=20)
        
        # Call button
        call_btn = tk.Button(
            button_frame,
            text="📞",
            font=('Arial', 24),
            bg='#4CAF50',
            fg='white',
            width=5,
            command=self.make_call
        )
        call_btn.pack(side=tk.RIGHT, padx=20)
        
    def add_digit(self, digit):
        """Add digit to phone number"""
        current = self.number_var.get()
        self.number_var.set(current + digit)
        
    def delete_digit(self):
        """Delete last digit"""
        current = self.number_var.get()
        if current:
            self.number_var.set(current[:-1])
            
    def make_call(self):
        """Make a phone call"""
        number = self.number_var.get()
        if number:
            messagebox.showinfo(
                "Calling",
                f"Calling {number}...\n\n"
                "(This is a simulation)\n"
                "In a real phone app, this would dial the number."
            )
            
            # Log the call
            self.os_app.db.log_event('phone_call', {
                'number': number,
                'time': time.time(),
                'user': self.os_app.current_user
            })
        else:
            messagebox.showwarning("No Number", "Please enter a phone number.")
            
    def switch_tab(self, tab_name):
        """Switch between tabs"""
        # Reset all tabs
        for tab, btn in self.tab_vars.items():
            btn.config(bg='#f5f5f5', fg='#333333')
            
        # Highlight current tab
        self.tab_vars[tab_name].config(bg='#4CAF50', fg='white')
        
        # Show appropriate content
        if tab_name == "Keypad":
            self.show_keypad()
        elif tab_name == "Recents":
            self.show_recents()
        elif tab_name == "Contacts":
            self.show_contacts()
        elif tab_name == "Voicemail":
            self.show_voicemail()
            
    def show_recents(self):
        """Show recent calls"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Sample recent calls
        recents = [
            ("John Doe", "📱", "(555) 123-4567", "Today 10:30", "incoming"),
            ("Jane Smith", "📞", "(555) 987-6543", "Today 09:15", "outgoing"),
            ("Mom", "📱", "(555) 111-2233", "Yesterday", "missed"),
            ("Work", "📞", "(555) 444-5566", "2 days ago", "outgoing"),
            ("Unknown", "📱", "(555) 999-8888", "3 days ago", "incoming")
        ]
        
        # Create list
        for name, icon, number, time_str, call_type in recents:
            call_frame = tk.Frame(self.content_frame, bg='white', height=60)
            call_frame.pack(fill=tk.X, pady=1)
            call_frame.pack_propagate(False)
            
            # Call type color
            if call_type == "missed":
                color = '#f44336'
            elif call_type == "outgoing":
                color = '#4CAF50'
            else:
                color = '#2196F3'
                
            # Icon
            icon_label = tk.Label(
                call_frame,
                text=icon,
                font=('Arial', 20),
                bg=color,
                fg='white',
                width=3
            )
            icon_label.pack(side=tk.LEFT, padx=10, pady=10)
            
            # Details
            details_frame = tk.Frame(call_frame, bg='white')
            details_frame.pack(side=tk.LEFT, fill=tk.Y, pady=10)
            
            tk.Label(
                details_frame,
                text=name,
                font=('Arial', 14, 'bold'),
                bg='white',
                fg='black',
                anchor=tk.W
            ).pack(anchor=tk.W)
            
            tk.Label(
                details_frame,
                text=f"{number} • {time_str}",
                font=('Arial', 10),
                bg='white',
                fg='#666666',
                anchor=tk.W
            ).pack(anchor=tk.W)
            
    def show_contacts(self):
        """Show contacts"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Sample contacts
        contacts = [
            ("👨", "John Doe", "(555) 123-4567"),
            ("👩", "Jane Smith", "(555) 987-6543"),
            ("👵", "Mom", "(555) 111-2233"),
            ("👨‍💼", "Work", "(555) 444-5566"),
            ("👨‍⚕️", "Doctor", "(555) 777-8899"),
            ("🚔", "Emergency", "911"),
            ("👮", "Police", "(555) 222-3333"),
            ("🔥", "Fire Department", "(555) 333-4444")
        ]
        
        # Create contacts list
        for icon, name, number in contacts:
            contact_frame = tk.Frame(self.content_frame, bg='white', height=60)
            contact_frame.pack(fill=tk.X, pady=1)
            contact_frame.pack_propagate(False)
            
            # Contact icon
            icon_label = tk.Label(
                contact_frame,
                text=icon,
                font=('Arial', 20),
                bg='#e0e0e0',
                fg='black',
                width=3
            )
            icon_label.pack(side=tk.LEFT, padx=10, pady=10)
            
            # Contact details
            details_frame = tk.Frame(contact_frame, bg='white')
            details_frame.pack(side=tk.LEFT, fill=tk.Y, pady=10)
            
            tk.Label(
                details_frame,
                text=name,
                font=('Arial', 14, 'bold'),
                bg='white',
                fg='black',
                anchor=tk.W
            ).pack(anchor=tk.W)
            
            tk.Label(
                details_frame,
                text=number,
                font=('Arial', 11),
                bg='white',
                fg='#666666',
                anchor=tk.W
            ).pack(anchor=tk.W)
            
            # Call button
            call_btn = tk.Button(
                contact_frame,
                text="📞",
                font=('Arial', 16),
                bg='#4CAF50',
                fg='white',
                width=3,
                command=lambda n=number: self.call_contact(n)
            )
            call_btn.pack(side=tk.RIGHT, padx=10)
            
    def call_contact(self, number):
        """Call a contact"""
        self.number_var.set(number)
        self.switch_tab("Keypad")
        
    def show_voicemail(self):
        """Show voicemail"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        tk.Label(
            self.content_frame,
            text="Voicemail",
            font=('Arial', 24, 'bold'),
            bg='white',
            fg='black'
        ).pack(pady=50)
        
        tk.Label(
            self.content_frame,
            text="No voicemails",
            font=('Arial', 16),
            bg='white',
            fg='#666666'
        ).pack(pady=10)
        
        tk.Label(
            self.content_frame,
            text="Your voicemail box is empty",
            font=('Arial', 12),
            bg='white',
            fg='#999999'
        ).pack(pady=5)