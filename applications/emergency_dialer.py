# applications/emergency_dialer.py
import tkinter as tk
from tkinter import messagebox

class EmergencyDialer:
    def __init__(self, parent, os_app):
        self.os_app = os_app
        self.parent = parent
        
        # Create emergency dialer
        self.window = tk.Toplevel(parent)
        self.window.title("Emergency Dialer")
        self.window.geometry("360x600")
        self.window.configure(bg='#000000')
        
        # Make fullscreen and on top
        self.window.attributes('-fullscreen', True)
        self.window.attributes('-topmost', True)
        
        self.setup_emergency_dialer()
        
    def setup_emergency_dialer(self):
        """Setup emergency dialer interface"""
        # Emergency banner
        banner_frame = tk.Frame(self.window, bg='#ff0000', height=100)
        banner_frame.pack(fill=tk.X)
        
        tk.Label(
            banner_frame,
            text="EMERGENCY CALL",
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#ff0000'
        ).pack(expand=True)
        
        # Instructions
        tk.Label(
            self.window,
            text="Swipe to call emergency services",
            font=('Arial', 16),
            fg='white',
            bg='#000000'
        ).pack(pady=20)
        
        # Emergency number display
        tk.Label(
            self.window,
            text="911",
            font=('Arial', 72, 'bold'),
            fg='white',
            bg='#000000'
        ).pack(pady=40)
        
        # Swipe to call button
        self.swipe_button = tk.Frame(self.window, bg='#333333', width=300, height=100)
        self.swipe_button.pack(pady=40)
        self.swipe_button.pack_propagate(False)
        
        tk.Label(
            self.swipe_button,
            text="Swipe to call →",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#333333'
        ).pack(expand=True)
        
        # Bind swipe motion
        self.swipe_button.bind('<B1-Motion>', self.handle_swipe)
        
        # Emergency contacts
        contacts_frame = tk.Frame(self.window, bg='#000000')
        contacts_frame.pack(fill=tk.X, pady=20, padx=20)
        
        emergency_contacts = [
            ("Police", "(555) 222-3333"),
            ("Fire Department", "(555) 333-4444"),
            ("Ambulance", "(555) 444-5555"),
            ("Poison Control", "(555) 555-6666")
        ]
        
        for name, number in emergency_contacts:
            contact_btn = tk.Button(
                contacts_frame,
                text=f"{name}\n{number}",
                font=('Arial', 12),
                bg='#222222',
                fg='white',
                command=lambda n=number: self.call_emergency(n)
            )
            contact_btn.pack(fill=tk.X, pady=5, ipady=10)
            
        # Cancel button
        cancel_btn = tk.Button(
            self.window,
            text="Cancel",
            font=('Arial', 16),
            bg='#666666',
            fg='white',
            command=self.window.destroy
        )
        cancel_btn.pack(pady=20, ipadx=30, ipady=10)
        
    def handle_swipe(self, event):
        """Handle swipe motion"""
        # Get button position
        x, y = event.x, event.y
        
        # If swiped enough to the right
        if x > 200:
            self.call_emergency("911")
            
    def call_emergency(self, number):
        """Call emergency number"""
        messagebox.showinfo(
            "Emergency Call",
            f"Calling {number}...\n\n"
            "EMERGENCY SERVICES DIALED\n\n"
            "(This is a simulation)\n"
            "In a real emergency, this would call actual emergency services."
        )
        
        # Log emergency call
        self.os_app.db.log_event('emergency_call', {
            'number': number,
            'user': self.os_app.current_user,
            'time': time.time()
        })
        
        self.window.destroy()