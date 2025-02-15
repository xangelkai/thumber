import sys
import os
import subprocess
import numpy as np
from PIL import Image
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QVBoxLayout, QMessageBox


class ThumbnailGenerator:
    """Class for generating video thumbnails (usable in both GUI and CLI)."""

    def __init__(self):
        pass

    def extract_thumbnails(self, video_file):
        """Extracts 12 frames from a video and arranges them in a 4x3 grid."""
        output_dir = os.path.dirname(video_file)  # Save in the same directory as the source video
        base_name = os.path.splitext(os.path.basename(video_file))[0]
        output_image = os.path.join(output_dir, f"{base_name}_preview.jpg")

        # Get video duration
        duration = self.get_video_duration(video_file)
        if not duration:
            print(f"Could not determine video duration: {video_file}")
            return None

        # Get 12 frames evenly spread across the video
        timestamps = np.linspace(0, duration, 12, endpoint=False)
        frames = [self.get_video_frame(video_file, t) for t in timestamps]

        # Remove None frames
        frames = [f for f in frames if f is not None]
        if not frames:
            print(f"Could not extract frames from video: {video_file}")
            return None

        # Create a 4x3 grid layout
        thumbnail = self.create_grid_image(frames, cols=4, rows=3)
        thumbnail.save(output_image)

        print(f"✅ Thumbnail saved: {output_image}")
        return output_image

    def get_video_duration(self, video_file):
        """Returns the duration of the video in seconds."""
        command = [
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_file
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            return float(result.stdout.strip())
        except ValueError:
            return None

    def get_video_frame(self, video_file, timestamp):
        """Extracts a frame from the video at a given timestamp."""
        output_frame = "frame.jpg"
        command = [
            "ffmpeg", "-ss", str(timestamp), "-i", video_file, "-frames:v", "1",
            "-q:v", "2", output_frame, "-y"
        ]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if os.path.exists(output_frame):
            frame = Image.open(output_frame)
            os.remove(output_frame)
            return frame
        return None

    def create_grid_image(self, images, cols, rows):
        """Creates a 4x3 grid of thumbnails."""
        width, height = images[0].size
        total_width = width * cols
        total_height = height * rows

        new_image = Image.new("RGB", (total_width, total_height))
        for i, img in enumerate(images):
            x = (i % cols) * width
            y = (i // cols) * height
            new_image.paste(img, (x, y))

        return new_image


class VideoThumbnailGenerator(QWidget):
    """Graphical user interface for generating video thumbnails."""

    def __init__(self):
        super().__init__()
        self.initUI()
        self.generator = ThumbnailGenerator()  # Create a generator instance

    def initUI(self):
        self.setWindowTitle("Video Thumbnail Generator")
        self.setGeometry(100, 100, 600, 450)

        layout = QVBoxLayout()
        self.label = QLabel("Select video files:")
        layout.addWidget(self.label)

        self.btn_select = QPushButton("Choose Videos")
        self.btn_select.clicked.connect(self.select_videos)
        layout.addWidget(self.btn_select)

        self.btn_generate = QPushButton("Generate Previews")
        self.btn_generate.clicked.connect(self.generate_thumbnails)
        layout.addWidget(self.btn_generate)

        self.setLayout(layout)
        self.video_files = []

    def select_videos(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Video Files", "", "Video Files (*.mp4 *.avi *.mov *.mkv)")
        if files:
            self.video_files = files
            self.label.setText(f"Selected files: {len(files)}")

    def generate_thumbnails(self):
        if not self.video_files:
            QMessageBox.warning(self, "Error", "Please select at least one video!")
            return

        for video in self.video_files:
            self.generator.extract_thumbnails(video)

        QMessageBox.information(self, "Done", "Previews have been generated!")


def run_cli():
    """CLI mode for generating thumbnails."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate video thumbnails (a grid of 12 frames) from video files.")
    parser.add_argument("videos", nargs="+", help="Path to video file(s)")
    args = parser.parse_args()

    generator = ThumbnailGenerator()

    for video in args.videos:
        if os.path.exists(video):
            generator.extract_thumbnails(video)
        else:
            print(f"❌ File not found: {video}")

    print("✅ Thumbnail generation completed!")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_cli()
    else:
        app = QApplication(sys.argv)
        window = VideoThumbnailGenerator()
        window.show()
        sys.exit(app.exec())
