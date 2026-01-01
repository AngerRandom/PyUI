import tkinter as tk
from tkinter import colorchooser, filedialog

class PaintApp:
    def __init__(self, parent, os_app):
        self.os_app = os_app
        self.parent = parent
        
        # Create paint window
        self.window = tk.Toplevel(parent)
        self.window.title("Paint")
        self.window.geometry("800x600")
        
        # Drawing variables
        self.current_tool = 'pencil'
        self.current_color = 'black'
        self.line_width = 2
        self.last_x = None
        self.last_y = None
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup paint UI"""
        # Toolbar
        toolbar = tk.Frame(self.window)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Tools
        tools = [
            ('Pencil', 'pencil'),
            ('Line', 'line'),
            ('Rectangle', 'rectangle'),
            ('Oval', 'oval'),
            ('Eraser', 'eraser'),
        ]
        
        for name, tool in tools:
            btn = tk.Button(
                toolbar,
                text=name,
                command=lambda t=tool: self.select_tool(t)
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            
        # Color selection
        color_btn = tk.Button(
            toolbar,
            text='Color',
            command=self.choose_color
        )
        color_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Line width
        tk.Label(toolbar, text='Width:').pack(side=tk.LEFT, padx=2, pady=2)
        self.width_scale = tk.Scale(
            toolbar,
            from_=1,
            to=20,
            orient=tk.HORIZONTAL,
            command=self.set_line_width
        )
        self.width_scale.set(self.line_width)
        self.width_scale.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Clear button
        clear_btn = tk.Button(
            toolbar,
            text='Clear',
            command=self.clear_canvas
        )
        clear_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Save button
        save_btn = tk.Button(
            toolbar,
            text='Save',
            command=self.save_image
        )
        save_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Canvas
        self.canvas = tk.Canvas(
            self.window,
            bg='white',
            cursor='cross'
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind events
        self.canvas.bind('<Button-1>', self.start_draw)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.stop_draw)
        
    def select_tool(self, tool):
        """Select drawing tool"""
        self.current_tool = tool
        
    def choose_color(self):
        """Choose drawing color"""
        color = colorchooser.askcolor(title='Choose color')[1]
        if color:
            self.current_color = color
            
    def set_line_width(self, value):
        """Set line width"""
        self.line_width = int(value)
        
    def clear_canvas(self):
        """Clear canvas"""
        self.canvas.delete('all')
        
    def save_image(self):
        """Save image"""
        file_path = filedialog.asksaveasfilename(
            defaultextension='.ps',
            filetypes=[('PostScript', '*.ps'), ('All files', '*.*')]
        )
        if file_path:
            try:
                self.canvas.postscript(file=file_path, colormode='color')
                self.os_app.logger.info(f"Image saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")
                
    def start_draw(self, event):
        """Start drawing"""
        self.last_x = event.x
        self.last_y = event.y
        
    def draw(self, event):
        """Draw on canvas"""
        if self.last_x and self.last_y:
            x, y = event.x, event.y
            
            if self.current_tool == 'pencil':
                self.canvas.create_line(
                    self.last_x, self.last_y, x, y,
                    fill=self.current_color,
                    width=self.line_width,
                    capstyle=tk.ROUND,
                    smooth=tk.TRUE
                )
                self.last_x = x
                self.last_y = y
                
            elif self.current_tool == 'eraser':
                self.canvas.create_line(
                    self.last_x, self.last_y, x, y,
                    fill='white',
                    width=self.line_width * 2,
                    capstyle=tk.ROUND
                )
                self.last_x = x
                self.last_y = y
                
    def stop_draw(self, event):
        """Stop drawing"""
        if self.last_x and self.last_y and self.current_tool in ['line', 'rectangle', 'oval']:
            x, y = event.x, event.y
            
            if self.current_tool == 'line':
                self.canvas.create_line(
                    self.last_x, self.last_y, x, y,
                    fill=self.current_color,
                    width=self.line_width
                )
            elif self.current_tool == 'rectangle':
                self.canvas.create_rectangle(
                    self.last_x, self.last_y, x, y,
                    outline=self.current_color,
                    width=self.line_width
                )
            elif self.current_tool == 'oval':
                self.canvas.create_oval(
                    self.last_x, self.last_y, x, y,
                    outline=self.current_color,
                    width=self.line_width
                )
        
        self.last_x = None
        self.last_y = None