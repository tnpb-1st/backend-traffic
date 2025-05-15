# Traffic Monitoring System

## 🔍 Overview

A sophisticated traffic analysis backend that leverages computer vision and machine learning to monitor and process traffic camera footage in real-time. This system detects, counts, and tracks vehicles across multiple traffic cameras, providing valuable insights into traffic patterns and density.

## ✨ Key Features

- **Automated Video Acquisition**: Downloads videos from multiple traffic cameras defined in a configuration file
- **Real-time Vehicle Detection**: Utilizes YOLOv5 to accurately identify cars, buses, and trucks in video streams
- **Concurrent Processing Pipeline**: Implements multi-threading for efficient processing of multiple video streams
- **RESTful API**: Exposes endpoints to retrieve processed video data and vehicle statistics
- **Scalable Architecture**: Designed to handle multiple camera groups with independent processing

## 🛠️ Technology Stack

- **Python**: Core programming language
- **YOLOv5**: State-of-the-art object detection model
- **OpenCV**: Computer vision library for video processing
- **Flask**: Lightweight web framework for API endpoints
- **Threading**: Parallel processing of video streams
- **FFmpeg**: Video conversion and manipulation
- **MoviePy**: Python library for video editing
- **JSON**: Data storage and API response format

## 🏗️ System Architecture

The system follows a modular design with distinct components:

1. **Video Downloader Module**
   - Fetches videos from configured traffic cameras
   - Handles network requests and error recovery
   - Organizes videos by camera groups

2. **Vehicle Detection Engine**
   - Processes video frames through YOLOv5
   - Identifies and counts vehicles by category
   - Generates annotated video output with detection boxes

3. **API Layer**
   - Provides endpoints for requesting processed data
   - Returns vehicle counts and processed videos
   - Supports filtering by camera group ID

## ⚡ Performance Optimizations

- Multi-threaded video processing for concurrent operations
- Efficient resource management through thread pooling
- Optimized video processing pipeline with intelligent frame handling
- JSON-based caching of results for quick retrieval

## 💎 Implementation Highlights

- **Concurrent Processing**: Uses threading to download and process multiple videos simultaneously
- **Error Handling**: Robust mechanisms to handle network failures and corrupt video files
- **Video Post-Processing**: Advanced processing including trimming and format conversion
- **Flexible Configuration**: JSON-based configuration for easy system adaptation

## 📦 Installation and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/backend-traffic.git
cd backend-traffic

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 🔌 API Usage

### Get Processed Video Data

```
GET /get?id=<camera_group_id>
```

Returns processed video data and vehicle counts for the specified camera group.

## 🚀 Future Enhancements

- Traffic density heatmaps
- Vehicle speed estimation
- Traffic anomaly detection
- Historical data analysis and pattern recognition
- Integration with traffic management systems

## 📄 License

[MIT License](LICENSE)
