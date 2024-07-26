import os
import json
import requests
import threading
from datetime import datetime
from moviepy.editor import VideoFileClip


# Function to get the current timestamp
def get_current_timestamp():
    return int(datetime.now().timestamp() * 1e9)


# Function to download a video
def download_video(camera_info, group_id, timestamp, download_dir):
    video_url = f"{camera_info['url']}?time={timestamp}"
    video_filename = f"{group_id}_{camera_info['camera']}_{timestamp}.mp4"
    video_path = os.path.join(download_dir, video_filename)

    response = requests.get(video_url)

    if response.status_code == 200:
        with open(video_path, "wb") as video_file:
            video_file.write(response.content)
        return video_path
    else:
        print(f"Error downloading video from {camera_info['name']}")
        return None


# Function to process a video and trim the last second if longer than 8 seconds
def process_video(video_path):
    try:
        clip = VideoFileClip(video_path)
        if clip.duration > 8:
            clip = clip.subclip(0, clip.duration - 1)
            processed_path = video_path.replace(".mp4", "_processed.mp4")
            clip.write_videofile(
                processed_path, codec="libx264", audio_codec="aac", bitrate="5000k"
            )
            os.remove(video_path)
            os.rename(processed_path, video_path)
        clip.close()
    except Exception as e:
        print(f"Error processing video {video_path}: {e}")


# Function to process the download of videos from a group of cameras
def process_camera_group(group_id, cameras, timestamp, download_dir, updated_cameras):
    for camera in cameras:
        video_path = download_video(camera, group_id, timestamp, download_dir)
        if video_path:
            process_video(video_path)
            camera["path"] = os.path.abspath(video_path)
        updated_cameras.append(camera)


# Main function to manage video downloads
def download_videos_pipeline():
    # Path to the JSON file and download directory
    json_file_path = "./cameras.json"
    download_dir = "downloaded_videos"

    # Create download directory if it doesn't exist
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Read the JSON file
    with open(json_file_path, "r") as json_file:
        camera_data = json.load(json_file)

    # Get the current timestamp
    timestamp = get_current_timestamp()

    # List to store threads and updated camera data
    threads = []
    updated_camera_data = {}

    # Start video download for each camera group
    for group_id, cameras in camera_data.items():
        updated_cameras = []
        updated_camera_data[group_id] = updated_cameras
        thread = threading.Thread(
            target=process_camera_group,
            args=(group_id, cameras, timestamp, download_dir, updated_cameras),
        )
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print(updated_camera_data)
    return updated_camera_data


# Test
if __name__ == "__main__":
    download_videos_pipeline()
