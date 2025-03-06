import os
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
import uuid
import cv2
import numpy as np

class MediaOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Organizer")
        self.root.geometry("500x400")  # Fixed size for the window

        self.media_files = []
        self.undo_stack = []
        self.current_file_index = 0
        self.max_undo_stack = 20

        self.sorted_folders_path = os.path.join(os.getcwd(), "Sorted_Media")
        self.media_folder = None
        self.video_capture = None
        self.video_frame = None

        # UI Elements
        self.canvas_width = 400
        self.canvas_height = 300

        self.canvas = tk.Canvas(self.root, bg="gray", width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.label = tk.Label(self.root, text="Select Folder", font=("Helvetica", 16))
        self.label.pack()

        self.button = tk.Button(self.root, text="Choose Folder", command=self.select_folder)
        self.button.pack(pady=10)

        self.file_info = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.file_info.pack()

        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<Control-n>", self.create_category_folder)
        self.root.bind("<Control-z>", self.undo_copy)

    def select_folder(self):
        """Let the user select a folder containing media files."""
        self.media_folder = filedialog.askdirectory(title="Select Folder")
        if self.media_folder:
            self.load_media_files()

    def load_media_files(self):
        """Load media files (images, videos, and audio) from the selected folder, excluding files in categorized folders."""
        self.media_files = []
        self.categorized_folders = set()

        self.update_lists()

        self.show_media()

    def update_lists(self):
        # Look for already existing categorized folders
        for folder in os.listdir(self.sorted_folders_path): #mark
            folder_path = os.path.join(self.sorted_folders_path, folder)
            if os.path.isdir(folder_path):
                self.categorized_folders.add(folder)

        for file in os.listdir(self.media_folder):
            file_path = os.path.join(self.media_folder, file)
            if os.path.isfile(file_path):
                # Skip files inside categorized folders
                if any(file_path.startswith(os.path.join(self.media_folder, cat_folder)) for cat_folder in self.categorized_folders):
                    continue
                
                if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
                    self.media_files.append(("image", file_path))
                elif file.lower().endswith(('mp4', 'avi', 'mov')):
                    self.media_files.append(("video", file_path))
                elif file.lower().endswith(('mp3', 'wav', 'flac')):
                    self.media_files.append(("audio", file_path))

        # Filter out any media already categorized
        self.filter_media_files_in_categories()

    def filter_media_files_in_categories(self):
        """Remove media files that already exist in categorized folders."""
        self.media_files = [
            (file_type, file_path) for file_type, file_path in self.media_files
            if not any(
                os.path.exists(os.path.join(self.sorted_folders_path, category, os.path.basename(file_path)))
                for category in self.categorized_folders
            )
        ]


    def show_media(self):
        """Display the current media file (image or video) on the GUI."""
        if not self.media_files:
            return

        file_type, file_path = self.media_files[self.current_file_index]

        self.canvas.delete("all")  # Clear canvas

        if file_type == "image":
            self.display_image(file_path)
        elif file_type == "video":
            self.show_video_preview(file_path)
        elif file_type == "audio":
            self.file_info.config(text=f"Audio: {os.path.basename(file_path)}")

    def display_image(self, file_path):
        """Display image on the canvas, fitting inside the fixed gray area, with correct orientation."""
        try:
            img = Image.open(file_path)

            # Get EXIF orientation
            exif = img._getexif()
            if exif:
                orientation = exif.get(0x0112, 1)  # 0x0112 is the EXIF Orientation tag ID
                if orientation == 3:
                    img = img.rotate(180, expand=True)
                elif orientation == 6:
                    img = img.rotate(270, expand=True)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)

            img.thumbnail((self.canvas_width, self.canvas_height))  # Resize while maintaining aspect ratio
            img_tk = ImageTk.PhotoImage(img)

            self.canvas.create_image(self.canvas_width // 2, self.canvas_height // 2, image=img_tk)
            self.canvas.image = img_tk  # Keep reference to image

            self.file_info.config(text=f"Image: {os.path.basename(file_path)}")
        except (AttributeError, KeyError, IndexError):
            # Cases: image doesn't have getexif or other errors
            self.file_info.config(text=f"Error loading image: {os.path.basename(file_path)}")

    def show_video_preview(self, video_path):
        """Show the first frame of the video with a red play icon."""
        if self.video_capture:
            self.video_capture.release()

        self.video_capture = cv2.VideoCapture(video_path)

        # Get the first frame
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)

            # Resize to fit within the canvas while maintaining aspect ratio
            img.thumbnail((self.canvas_width, self.canvas_height))
            img_tk = ImageTk.PhotoImage(img)

            self.canvas.create_image(self.canvas_width // 2, self.canvas_height // 2, image=img_tk)
            self.canvas.image = img_tk  # Keep reference to image

            # Draw the play button in the top-right corner
            self.draw_play_button()

            self.file_info.config(text=f"Video: {os.path.basename(video_path)}")

    def draw_play_button(self):
        """Draw a red play button in the top-right corner."""
        play_button_radius = 30  # Radius of the circle
        triangle_size = 10  # Size of the play triangle

        # Coordinates for the play button
        center_x = self.canvas_width - 50  # 800 (width of canvas) - 50 (margin)
        center_y = 50   # 50px from the top

        # Draw the red circle (play button background)
        play_button_id = self.canvas.create_oval(center_x - play_button_radius, center_y - play_button_radius,
                                                  center_x + play_button_radius, center_y + play_button_radius,
                                                  fill="red", outline="red")
        
        # Draw the triangle (play symbol) inside the circle
        points = [center_x - triangle_size, center_y - triangle_size,
                  center_x - triangle_size, center_y + triangle_size,
                  center_x + triangle_size, center_y]
        self.canvas.create_polygon(points, fill="white", outline="white")
        
        # Bind the play button click to the open_video_player method
        self.canvas.tag_bind(play_button_id, "<Button-1>", self.open_video_player)

    def open_video_player(self, event):
        """Open the video with the system's default player."""
        if self.video_capture and self.video_capture.isOpened():
            video_path = self.media_files[self.current_file_index][1]  # Get current video path

            # Use subprocess to open the default video player
            import subprocess
            if os.name == 'nt':  # For Windows
                subprocess.run(["start", video_path], shell=True)
            elif os.name == 'posix':  # For macOS/Linux
                subprocess.run(["xdg-open", video_path])

    def on_key_press(self, event):
        """Handle keyboard events for moving files, creating folders, and undo."""
        if event.keysym == 'Escape':
            self.root.quit()
        elif event.char.isdigit() and event.char in '1234567890':
            self.copy_file_to_category(int(event.char))

    def copy_file_to_category(self, category_number):
        """Copy the current file to a numbered folder."""
        if not self.media_files:
            return

        file_type, file_path = self.media_files[self.current_file_index]
        sorted_folder = os.path.join(os.getcwd(), "Sorted_Media")

        if not os.path.exists(sorted_folder):
            os.makedirs(sorted_folder)

        # Now we consider folders that may contain both the number and description.
        category_folder = os.path.join(sorted_folder, f"Category_{category_number}")
        category_folders_with_description = [folder for folder in os.listdir(sorted_folder)
                                             if folder.startswith(f"Category_{category_number}_")]
        
        if category_folders_with_description:
            category_folder = os.path.join(sorted_folder, category_folders_with_description[0])
        
        if not os.path.exists(category_folder):
            return  # Don't create category folder if it doesn't exist

        file_name = os.path.basename(file_path)
        new_file_path = os.path.join(category_folder, file_name)

        # Avoid overwriting files by renaming
        if os.path.exists(new_file_path):
            new_file_path = os.path.join(category_folder, f"{file_name}")

        shutil.copy(file_path, new_file_path)  # Change to copy

        # Push to undo stack
        self.undo_stack.append(("copy", file_path, new_file_path))
        if len(self.undo_stack) > self.max_undo_stack:
            self.undo_stack.pop(0)

        # Go to next media
        self.current_file_index += 1
        if self.current_file_index >= len(self.media_files):
            self.update_lists()
            self.current_file_index = 0

        self.show_media()

    def create_category_folder(self, event=None):
        """Create a new category folder with a user-defined description."""
        sorted_folder = os.path.join(os.getcwd(), "Sorted_Media")
        if not os.path.exists(sorted_folder):
            os.makedirs(sorted_folder)

        # Find the next available category number
        existing_categories = [f for f in os.listdir(sorted_folder) if f.startswith("Category_")]
        category_numbers = []
        for category in existing_categories:
            # Extract category number from folder name, assuming format "Category_<number>"
            try:
                category_number = int(category.split("_")[1])
                category_numbers.append(category_number)
            except ValueError:
                continue

        next_category_number = 1
        while next_category_number in category_numbers:
            next_category_number += 1

        description = simpledialog.askstring("Category Description", f"Enter description for new category {next_category_number}:")
        if description:
            category_folder = os.path.join(sorted_folder, f"Category_{next_category_number}_{description}")
            if not os.path.exists(category_folder):
                os.makedirs(category_folder)

    def undo_copy(self, event=None):
        """Undo the last copy operation.""" 
        if not self.undo_stack: 
            return

        action, src, dest = self.undo_stack.pop()

        if action == "copy":
            os.remove(dest)  # Remove the copied file 
            self.show_undo_message(src)
            self.current_file_index -= 1
        self.show_media()
        

    def show_undo_message(self, file_path): 
        """Display the undone action message.""" 
        file_name = os.path.basename(file_path) 
        self.file_info.config(text=f"Undid: {file_name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MediaOrganizerApp(root)
    root.mainloop()
