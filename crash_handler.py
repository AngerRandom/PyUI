# crash_handler.py
import tkinter as tk
from tkinter import ttk
import traceback
import time
import random

class CrashHandler:
    def __init__(self, os_app):
        self.os_app = os_app
        self.crash_styles = [
            'blue_screen',
            'kernel_panic',
            'segfault',
            'bsod'
        ]
        
    def show_crash_screen(self, app_name="Unknown", error_message="System crash", 
                         style=None, details=None):
        """Show crash screen"""
        if style is None:
            style = random.choice(self.crash_styles)
            
        if style == 'blue_screen':
            self.show_bsod(app_name, error_message, details)
        elif style == 'kernel_panic':
            self.show_kernel_panic(app_name, error_message, details)
        elif style == 'segfault':
            self.show_segfault(app_name, error_message, details)
        else:
            self.show_bsod(app_name, error_message, details)
            
    def show_bsod(self, app_name, error_message, details=None):
        """Show Blue Screen of Death"""
        crash_window = tk.Toplevel(self.os_app.root)
        crash_window.title("System Crash")
        crash_window.attributes('-fullscreen', True)
        crash_window.configure(bg='#0000aa')
        
        # Make it modal
        crash_window.grab_set()
        crash_window.focus_force()
        
        # BSOD content
        content = f"""A problem has been detected and the system has been shut down 
to prevent damage to your computer.

{error_message}

If this is the first time you've seen this error screen,
restart your computer. If this screen appears again, follow
these steps:

Check to make sure any new hardware or software is properly installed.
If this is a new installation, ask your hardware or software manufacturer
for any system updates you might need.

Technical information:

*** STOP: 0x0000007B (0xF78D2524, 0xC0000034, 0x00000000, 0x00000000)

***   {app_name}.exe - Address F78D2524 base at F78D2000, DateStamp 3dd9919eb

Beginning dump of physical memory
Physical memory dump complete.
Contact your system administrator or technical support group for further assistance.
"""
        
        text_widget = tk.Text(
            crash_window,
            bg='#0000aa',
            fg='white',
            font=('Lucida Console', 14),
            wrap=tk.WORD,
            borderwidth=0,
            highlightthickness=0
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
        
        # Add details if provided
        if details:
            details_text = tk.Text(
                crash_window,
                bg='#0000aa',
                fg='#cccccc',
                font=('Courier New', 10),
                height=10
            )
            details_text.pack(fill=tk.X, padx=50, pady=(0, 50))
            details_text.insert(tk.END, f"Debug Details:\n{details}")
            details_text.config(state=tk.DISABLED)
        
        # Auto-restart timer
        self.restart_timer(crash_window, 10)
        
    def show_kernel_panic(self, app_name, error_message, details=None):
        """Show kernel panic screen (Linux style)"""
        crash_window = tk.Toplevel(self.os_app.root)
        crash_window.title("Kernel Panic")
        crash_window.attributes('-fullscreen', True)
        crash_window.configure(bg='white')
        
        crash_window.grab_set()
        crash_window.focus_force()
        
        # Kernel panic content
        content = f"""Kernel panic - not syncing: {error_message}

CPU: 0 PID: {random.randint(1000, 9999)} Comm: {app_name}
Call Trace:
 [<ffffffff810a3b8a>] panic+0x1cb/0x3e8
 [<ffffffff8152b982>] oops_end+0x98/0xa0
 [<ffffffff8106a8a9>] no_context+0xfc/0x260
 [<ffffffff8106ab6a>] __bad_area_nosemaphore+0x141/0x1e0
 [<ffffffff8106ac06>] bad_area_nosemaphore+0xe/0x10
 [<ffffffff8106b2e8>] do_page_fault+0x2b8/0x4e0
 [<ffffffff81534b58>] page_fault+0x28/0x30

---[ end trace {random.randint(1000000000000000, 9999999999999999)} ]---
Kernel Offset: disabled
"""
        
        text_widget = tk.Text(
            crash_window,
            bg='white',
            fg='black',
            font=('Courier New', 12),
            wrap=tk.WORD
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
        
        self.restart_timer(crash_window, 8)
        
    def show_segfault(self, app_name, error_message, details=None):
        """Show segmentation fault screen"""
        crash_window = tk.Toplevel(self.os_app.root)
        crash_window.title("Segmentation Fault")
        crash_window.geometry("600x400")
        crash_window.configure(bg='#2c3e50')
        
        crash_window.grab_set()
        crash_window.focus_force()
        
        frame = tk.Frame(crash_window, bg='#2c3e50', padx=30, pady=30)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            frame,
            text="⚠️ Segmentation Fault",
            font=('Arial', 24, 'bold'),
            fg='#e74c3c',
            bg='#2c3e50'
        ).pack(pady=(0, 20))
        
        tk.Label(
            frame,
            text=f"Application '{app_name}' has crashed",
            font=('Arial', 14),
            fg='white',
            bg='#2c3e50'
        ).pack(pady=(0, 10))
        
        tk.Label(
            frame,
            text=error_message,
            font=('Courier', 11),
            fg='#ecf0f1',
            bg='#34495e',
            wraplength=500,
            justify=tk.LEFT,
            padx=10,
            pady=10
        ).pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        btn_frame = tk.Frame(frame, bg='#2c3e50')
        btn_frame.pack()
        
        tk.Button(
            btn_frame,
            text="Close Application",
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=10,
            command=crash_window.destroy
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Restart System",
            bg='#3498db',
            fg='white',
            padx=20,
            pady=10,
            command=self.os_app.restart_system
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Send Report",
            bg='#2ecc71',
            fg='white',
            padx=20,
            pady=10,
            command=lambda: self.send_crash_report(app_name, error_message, details)
        ).pack(side=tk.LEFT, padx=5)
        
    def restart_timer(self, window, seconds):
        """Show countdown and restart"""
        timer_label = tk.Label(
            window,
            text=f"System will restart in {seconds} seconds...",
            font=('Arial', 12),
            bg=window.cget('bg'),
            fg='yellow'
        )
        timer_label.pack(side=tk.BOTTOM, pady=20)
        
        def update_timer(count):
            if count > 0:
                timer_label.config(text=f"System will restart in {count} seconds...")
                window.after(1000, lambda: update_timer(count - 1))
            else:
                window.destroy()
                self.os_app.restart_system()
                
        update_timer(seconds)
        
    def send_crash_report(self, app_name, error_message, details):
        """Send crash report (simulated)"""
        self.os_app.db.log_event('crash_report', {
            'app': app_name,
            'error': error_message,
            'details': details,
            'timestamp': time.time()
        })
        
        messagebox.showinfo("Crash Report", "Crash report has been sent. Thank you!")