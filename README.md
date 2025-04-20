# Media Organizer App

The **Media Organizer App** is a powerful and user-friendly tool for organizing and managing various types of media files (images, videos, and audio). The app allows you to quickly and efficiently organize your media files into categorized folders with intuitive controls and a simple graphical user interface (GUI) built using Tkinter.

## Features

- **Multi-format Media Support**: 
  - **Images**: JPG, PNG, GIF, etc.
  - **Videos**: MP4, AVI, MOV.
  - **Audio**: MP3, WAV, FLAC.
  
- **Folder Selection**: Select a folder to load and view your media files.
  
- **Automatic Media Detection**: 
  - Automatically detects and categorizes media files while excluding those already placed in categorized folders.
  
- **Image Display**: 
  - Images are displayed with their correct orientation using EXIF data.
  - The images are resized to fit within the window, maintaining the aspect ratio.
  
- **Video Preview**: 
  - Displays the first frame of a video along with a red play button.
  - Option to open videos in the system’s default video player.

- **Audio File Display**: Displays audio files with their filenames for easy identification.

- **Category Management**: 
  - Create custom categories with user-defined descriptions.
  - Categories are automatically numbered.
  
- **File Movement**: 
  - Press number keys (1-9) to move files to the corresponding category.

- **Undo Functionality**: 
  - Undo the last move or copy operation.

- **Keyboard Shortcuts**:
  - `Escape`: Close the app.
  - `Number keys (1-9)`: Move the current file to the corresponding category.
  - `Ctrl + N`: Create a new category with a description.
  - `Ctrl + Z`: Undo the last copy action.

## Requirements

- Python 3.x
- Required Libraries:
  - `Pillow`
  - `opencv-python`
  - `tkinter`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Goko12346/Media-Organizer.git

2. Install the required libraries:

   ```bash
   pip install -r requirements.txt

3. Run the app:

   ```bash
   python main.py


## Usage

1. **Select Folder**:
   - After launching the app, you will be prompted to select a folder containing your media files (images, videos, or audio).
   - Choose the folder, and the app will automatically load and display all the media files in that folder, excluding files that are already categorized into sorted folders.

2. **Organize Media Files**:
   - The media files will be displayed in the main window.
   - You can organize these files into categories by pressing the number keys (1-9) to move the current file to the corresponding category folder.
   
3. **Create New Categories**:
   - Press `Ctrl + N` to create a new category.
   - The app will prompt you to enter a description for the new category (e.g., "Vacation", "Family", etc.).
   - Once you add the description, the category is created, and you can move files into it.

4. **Undo Operation**:
   - If you made a mistake, you can undo the last move or copy operation by pressing `Ctrl + Z`.
   - This will remove the last copied file and display a message showing which file was undone.

5. **Viewing Files**:
   - **Images**: The app displays images with their correct orientation (using EXIF data) and resized to fit within the canvas, maintaining aspect ratio.
   - **Videos**: Videos show the first frame with a red play button that you can click to open the video in your system's default player.
   - **Audio**: Audio files are displayed with their filenames.

6. **Closing the App**:
   - You can close the app anytime by pressing the `Escape` key.

## Features Recap

- **Multi-format media support**: Handle various media files (images, videos, and audio).
- **Automatic media detection**: Skips files already sorted into categorized folders.
- **Media file previews**: View images, videos (first-frame preview), and audio filenames.
- **Category management**: Easily create custom categories with descriptions.
- **File organization**: Move files into categories using number keys (1-9).
- **Undo functionality**: Undo the last file move operation with `Ctrl + Z`.

## Customization

You can extend and modify the app to suit your needs. For example, you can add support for more media formats or integrate additional file management features. The code is simple and modular, so it’s easy to add new functionality.

### Example Use Cases:

- **Organizing Photos**: Create categories like "Vacation", "Family", or "Work" and organize your images accordingly.
- **Managing Videos**: Sort video files by project or genre and preview them with the built-in frame preview.
- **Audio Collection**: Create categories for different types of audio files like music, podcasts, or sound effects.

## Contributions

Contributions are welcome! If you have an idea for a feature or want to fix a bug, feel free to submit an issue or pull request.

### How to contribute:
1. Fork the repository.
2. Create a branch (`git checkout -b feature-name`).
3. Implement your feature or fix.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to your branch (`git push origin feature-name`).
6. Submit a pull request.

## License

**Media-Organizer © 2025 by Goko12346** is licensed under the **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License**.

To view a copy of this license, visit: [Creative Commons License](https://creativecommons.org/licenses/by-nc-nd/4.0/).

This means:
- You can share the software, but you cannot use it for commercial purposes.
- You are not allowed to modify or distribute the software.
- Proper attribution is required when sharing the software.

## Acknowledgements

- **Tkinter**: The Python library for creating the GUI.
- **Pillow**: Python Imaging Library (PIL) fork for image handling and manipulation.
- **OpenCV**: A library used for video processing and preview functionality.

---

**Enjoy organizing your media files effortlessly with the Media Organizer App!** 🎉
