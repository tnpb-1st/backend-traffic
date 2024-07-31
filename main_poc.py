import subprocess
import os
import time
from flask import Flask, request, send_file, jsonify
from video_downloader import download_videos_pipeline
from vehicles_detector import process_videos_pipeline

app = Flask(__name__)

# Path to the directory where videos are stored
VIDEO_DIRECTORY = "a/path/to/your/public/data"  # Replace with the actual path

def auto_process_video(id, videos_dict):
    selected_videos_dict = {f"{id}": videos_dict[id]}
    processed_videos_dict = process_videos_pipeline(selected_videos_dict, VIDEO_DIRECTORY, id)

    # Create a simple response to send the videos
    response = processed_videos_dict
    return jsonify(response)

if __name__ == "__main__":
    # Clone the YOLOv5 repository
    repo_url = "https://github.com/ultralytics/yolov5.git"
    clone_dir = "yolov5"
    if not os.path.exists(clone_dir):
        result = subprocess.run(
            ["git", "clone", repo_url], capture_output=True, text=True
        )
        if result.returncode == 0:
            print("Successfully cloned YOLOv5 repository.")
        else:
            print("Failed to clone YOLOv5 repository.")
            print(result.stderr)

    # Ensure the processed_videos directory exists
    if not os.path.exists("processed_videos"):
        os.makedirs("processed_videos")

    with app.app_context():
        while True:
            videos_dict = download_videos_pipeline()
            for i in range(1, 6):
                auto_process_video(str(i), videos_dict)
            time.sleep(300)
