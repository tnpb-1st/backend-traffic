import subprocess
import os
import time
from flask import Flask, request, send_file, jsonify
from video_downloader import download_videos_pipeline
from vehicles_detector import process_videos_pipeline

app = Flask(__name__)

# Path to the directory where videos are stored
VIDEO_DIRECTORY = "a/path/to/your/public/data"  # Replace with the actual path


@app.route("/get", methods=["GET"])
def get_videos():
    video_id = request.args.get("id")
    if not video_id:
        return jsonify({"error": "No id parameter provided"}), 400

    videos_dict = download_videos_pipeline()
    selected_videos_dict = {f"{video_id}": videos_dict[video_id]}
    processed_videos_dict = process_videos_pipeline(selected_videos_dict, VIDEO_DIRECTORY, video_id)

    # Create a simple response to send the videos
    response = processed_videos_dict
    return jsonify(response)

def get_videos():
    video_id = request.args.get("id")
    if not video_id:
        return jsonify({"error": "No id parameter provided"}), 400

    videos_dict = download_videos_pipeline()
    selected_videos_dict = {f"{video_id}": videos_dict[video_id]}
    processed_videos_dict = process_videos_pipeline(selected_videos_dict, VIDEO_DIRECTORY, video_id)

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

    app.run(host="0.0.0.0", port=35435)