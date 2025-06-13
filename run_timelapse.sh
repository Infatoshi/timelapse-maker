#!/bin/bash

# This script automates the process of capturing a 24-hour timelapse
# and creating a video from the captured images.

# Exit immediately if a command exits with a non-zero status.
set -e

# Define directory paths
PROJECT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
IMG_DIR="$PROJECT_DIR/timelapse_imgs"
VIDEO_DIR="$PROJECT_DIR/videos"

# Create necessary directories if they don't exist
mkdir -p "$IMG_DIR"
mkdir -p "$VIDEO_DIR"

# Generate video filename at the start of the capture period.
# Format: YYYY_monDD.mp4 (e.g., 2024_jul18.mp4)
VIDEO_FILENAME="$(date +%Y_%b%d).mp4"
VIDEO_PATH="$VIDEO_DIR/$VIDEO_FILENAME"

# It's good practice to clean the image directory before starting a new capture.
# This removes any leftover images from a previous run.
echo "Cleaning up old images from $IMG_DIR..."
rm -f "$IMG_DIR"/*.jpg
echo "Cleanup complete."

# Run the capture script for 24 hours with a 12-second interval.
echo "Starting 24-hour timelapse capture..."
# Make sure to use the python3 interpreter. On some systems, 'python' might be python2.
# Using absolute paths for scripts and directories.
python3 "$PROJECT_DIR/capture_timelapse.py" --hours 24 --interval 12 --output-dir "$IMG_DIR"
echo "Timelapse capture finished."

# After capture is complete, create the video.
echo "Creating timelapse video: $VIDEO_PATH"
python3 "$PROJECT_DIR/create_timelapse.py" "$IMG_DIR" "$VIDEO_PATH"

echo "Timelapse process completed successfully. Video saved to $VIDEO_PATH" 