import cv2
import torch
import numpy as np
import os
import sys


def yolov5_detect(video_path, video_name, output_folder="processed_videos"):
    """
    Process the input video with YOLOv5, draw bounding boxes around detected vehicles,
    save the processed video, and return the processed video path and number of vehicles detected per frame.

    :param video_path: Path to the input video.
    :param video_name: Name of the video.
    :param output_folder: Folder to save the processed video.
    :return: Tuple (processed_video_path, number_vehicles_per_frame)
    """
    # Set up YOLOv5 path
    yolov5_path = os.path.join(os.getcwd(), "yolov5")

    # Load YOLOv5 model from torch hub
    model = torch.hub.load(
        "ultralytics/yolov5", "yolov5s", source="github", pretrained=True
    )
    model.eval()

    # Create output folder if not exists
    os.makedirs(output_folder, exist_ok=True)

    # Load video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video file {video_path}")

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for output video

    # Create output video file
    processed_video_path = os.path.join(output_folder, f"{video_name}_processed.mp4")
    out = cv2.VideoWriter(processed_video_path, fourcc, fps, (width, height))

    number_vehicles_per_frame = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Prepare frame for YOLOv5
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model(img)
        detections = results.pandas().xyxy[0]

        num_vehicles = 0
        for _, row in detections.iterrows():
            if row["class"] in [
                2,
                5,
                7,
            ]:  # Car, Bus, Truck class IDs (for COCO dataset)
                x1, y1, x2, y2 = (
                    int(row["xmin"]),
                    int(row["ymin"]),
                    int(row["xmax"]),
                    int(row["ymax"]),
                )
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                num_vehicles += 1

        number_vehicles_per_frame.append(num_vehicles)

        # Write frame to output video
        out.write(frame)

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return processed_video_path, number_vehicles_per_frame


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python yolov5_detect.py <video_path> <video_name>")
        sys.exit(1)

    video_path = sys.argv[1]
    video_name = sys.argv[2]
    processed_video_path, number_vehicles = yolov5_detect(video_path, video_name)

    print(f"Processed video saved to: {processed_video_path}")
    print(f"Number of vehicles detected per frame: {number_vehicles}")
