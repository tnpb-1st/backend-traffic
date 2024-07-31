import os
import threading
import cv2
import torch
from pathlib import Path
import queue
import ffmpeg
import json
from video_downloader import download_videos_pipeline

# Load the YOLOv5 model
model = torch.hub.load(
    "ultralytics/yolov5", "yolov5s"
)  # You can replace 'yolov5s' with any model variant

# Define the classes of interest (vehicles)
classes_of_interest = [2, 5, 7]  # 2: car, 5: bus, 7: truck


def process_video(video_info, output_path, id, result_queue):
    input_path = video_info["path"]
    tmp_path = os.path.join("tmp", os.path.basename(input_path))
    output_camera_path = os.path.join(output_path, "cameras", str(id))

    os.makedirs("tmp", exist_ok=True)
    os.makedirs(output_camera_path, exist_ok=True)

    output_video_path = os.path.join(output_camera_path, os.path.basename(input_path))

    # Open video capture
    cap = cv2.VideoCapture(input_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count // fps

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = None
    number_vehicles = [0] * (duration + 1)

    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process the frame with YOLOv5
        results = model(frame)

        # Filter results to include only the classes of interest
        detections = results.xyxy[0]
        vehicles = [d for d in detections if int(d[5]) in classes_of_interest]

        # Calculate the second of the current frame
        second = frame_idx // fps
        if frame_idx % fps == 0:
            number_vehicles[second] = len(vehicles)

        # Draw bounding boxes on the frame
        for det in vehicles:
            x1, y1, x2, y2, conf, cls = det
            label = f"{model.names[int(cls)]} {conf:.2f}"
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(
                frame,
                label,
                (int(x1), int(y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

        # Initialize video writer
        if out is None:
            out = cv2.VideoWriter(
                tmp_path, fourcc, fps, (frame.shape[1], frame.shape[0])
            )

        out.write(frame)
        frame_idx += 1

    cap.release()
    out.release()

    # Update the video_info dictionary
    convert_mpv4_to_mp4(tmp_path, output_video_path)
    video_info["processed_video_path"] = os.path.abspath(output_video_path)
    video_info["number_vehicles"] = number_vehicles
    result_queue.put(video_info)


def convert_mpv4_to_mp4(input_path, output_path):
    """
    Converts a video from MPV4 to MP4 using the H.264 codec.

    Parameters:
    input_path (str): The path to the input MPV4 file.
    output_path (str): The path to save the output MP4 file.
    """
    try:
        (
            ffmpeg.input(input_path)
            .output(
                output_path, vcodec="libx264", acodec="aac", y=None
            )  # 'y=None' to overwrite existing file
            .run(overwrite_output=True)
        )
        print(f"Conversion successful: {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def process_videos_pipeline(videos_dict, output_path, id):
    threads = []
    general_dict = { f"{id}": [] }
    result_queue = queue.Queue()
    for key, videos in videos_dict.items():
        for video_info in videos:
            t = threading.Thread(target=process_video, args=(video_info, output_path, id, result_queue))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()

    while not result_queue.empty():
        result = result_queue.get()
        general_dict[f"{id}"].append(result)

    output_info_path = os.path.join(output_path, "info")
    os.makedirs(output_info_path, exist_ok=True)
    # Save video_info as JSON
    json_output_path = os.path.join(output_info_path, f"{id}.json")
    with open(json_output_path, "w") as json_file:
        json.dump(general_dict, json_file, indent=4)

    return general_dict


# test
if __name__ == "__main__":
    videos_dict = download_videos_pipeline()
    process_videos_pipeline(videos_dict)
