# 🎬 Video Thumbnail Generator

**Video Thumbnail Generator** is a tool for generating preview images (grids of 12 frames) from video files. It works in both **Graphical User Interface (GUI)** and **Command Line Interface (CLI)** modes.

## 🚀 Features

✅ Extracts 12 evenly spaced frames from a video.  
✅ Creates a 4x3 grid from the extracted frames.  
✅ Supports popular video formats: `.mp4`, `.avi`, `.mov`, `.mkv`.  
✅ Graphical interface built with PyQt6.  
✅ CLI support for batch processing.  

## 📌 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/video-thumbnail-generator.git
cd video-thumbnail-generator
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Ensure `ffmpeg` and `ffprobe` are Installed
This tool uses `ffmpeg` for video processing. Make sure it is installed on your system.

## 🎮 Usage

### GUI Mode
Run the script without arguments to open the graphical interface:
```bash
python main.py
```
1. Click **"Choose Videos"** and select one or more video files.
2. Click **"Generate Previews"** to process the selected videos.
3. The preview images will be saved in the same directory as the videos.

### CLI Mode
You can also run the program in command-line mode:
```bash
python main.py path/to/video.mp4
```
For batch processing:
```bash
python main.py video1.mp4 video2.mkv video3.avi
```
Each generated preview image will be saved in the same directory as its corresponding video.

## 🛠 Requirements

- Python 3.8+
- `ffmpeg` and `ffprobe`
- Required Python packages (installed via `pip install -r requirements.txt`)

## 📜 License

This project is licensed under the MIT License.
