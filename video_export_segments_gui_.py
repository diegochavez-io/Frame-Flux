import tkinter as tk
from tkinter import filedialog
import os
import subprocess

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Video Clipper")

        # Create labels and entry fields for parameters
        tk.Label(self.window, text="Video file path:").pack()
        self.video_file_path_entry = tk.Entry(self.window, width=50)
        self.video_file_path_entry.pack()
        tk.Label(self.window, text="Clip duration (seconds):").pack()
        self.clip_duration_entry = tk.Entry(self.window, width=10)
        self.clip_duration_entry.pack()
        tk.Label(self.window, text="Number of clips to export:").pack()
        self.num_clips_entry = tk.Entry(self.window, width=10)
        self.num_clips_entry.pack()
        tk.Label(self.window, text="Output directory:").pack()
        self.output_directory_entry = tk.Entry(self.window, width=50)
        self.output_directory_entry.pack()

        # Create a button to start the video clipper
        self.start_button = tk.Button(self.window, text="Start", command=self.start_clipper)
        self.start_button.pack()

        # Create a button to select the video file
        self.select_button = tk.Button(self.window, text="Select video file", command=self.select_video_file)
        self.select_button.pack()

        self.window.mainloop()

    def select_video_file(self):
        self.video_file_path_entry.delete(0, tk.END)
        self.video_file_path_entry.insert(0, filedialog.askopenfilename())

    def start_clipper(self):
        video_file_path = self.video_file_path_entry.get()
        clip_duration = int(self.clip_duration_entry.get())
        num_clips = int(self.num_clips_entry.get())
        output_directory = self.output_directory_entry.get()

        # Call the trim_video function
        trim_video(video_file_path, clip_duration, output_directory, num_clips)

if __name__ == "__main__":
    gui = GUI()