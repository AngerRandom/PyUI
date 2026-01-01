# applications/media_player.py
import tkinter as tk
from tkinter import filedialog
import pygame
import os

class MediaPlayer:
    def __init__(self, parent, os_app):
        self.os_app = os_app
        self.parent = parent
        self.playing = False
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Media Player")
        self.window.geometry("500x400")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup media player UI"""
        # Control frame
        control_frame = tk.Frame(self.window)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Buttons
        self.play_btn = tk.Button(
            control_frame,
            text="▶",
            font=('Arial', 14),
            width=3,
            command=self.play_pause
        )
        self.play_btn.pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            control_frame,
            text="⏹",
            font=('Arial', 14),
            width=3,
            command=self.stop
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            control_frame,
            text="📁",
            font=('Arial', 14),
            width=3,
            command=self.load_file
        ).pack(side=tk.LEFT, padx=2)
        
        # Volume
        tk.Label(control_frame, text="Volume:").pack(side=tk.LEFT, padx=(20, 5))
        self.volume_scale = tk.Scale(
            control_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=self.set_volume,
            length=100
        )
        self.volume_scale.set(70)
        self.volume_scale.pack(side=tk.LEFT)
        
        # Display
        display_frame = tk.Frame(self.window, bg='black', height=200)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.display_label = tk.Label(
            display_frame,
            text="No media loaded",
            fg='white',
            bg='black'
        )
        self.display_label.pack(expand=True)
        
        # Playlist
        playlist_frame = tk.Frame(self.window)
        playlist_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tk.Label(playlist_frame, text="Playlist:").pack(anchor=tk.W)
        
        self.playlist = tk.Listbox(playlist_frame, height=8)
        self.playlist.pack(fill=tk.BOTH, expand=True)
        
        # Load sample music
        self.load_sample_playlist()
        
    def load_sample_playlist(self):
        """Load sample playlist"""
        sample_tracks = [
            "Track 1 - Sample Audio",
            "Track 2 - Test Sound",
            "Track 3 - Demo Music"
        ]
        
        for track in sample_tracks:
            self.playlist.insert(tk.END, track)
            
    def play_pause(self):
        """Play or pause media"""
        if not self.playing:
            self.playing = True
            self.play_btn.config(text="⏸")
            # In a real implementation, play actual audio
            self.display_label.config(text="Playing...")
        else:
            self.playing = False
            self.play_btn.config(text="▶")
            self.display_label.config(text="Paused")
            
    def stop(self):
        """Stop media"""
        self.playing = False
        self.play_btn.config(text="▶")
        self.display_label.config(text="Stopped")
        
    def load_file(self):
        """Load media file"""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ('Audio files', '*.mp3 *.wav *.ogg'),
                ('Video files', '*.mp4 *.avi *.mkv'),
                ('All files', '*.*')
            ]
        )
        
        if file_path:
            filename = os.path.basename(file_path)
            self.display_label.config(text=f"Loaded: {filename}")
            
    def set_volume(self, value):
        """Set volume"""
        volume = int(value) / 100
        pygame.mixer.music.set_volume(volume)