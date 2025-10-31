#!/bin/bash

# This script automates the process of capturing a 24-hour timelapse
# and creating a video from the captured images.

# Exit immediately if a command exits with a non-zero status.
set -e

# Define directory paths
PROJECT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
IMG_DIR="$PROJECT_DIR/timelapse_imgs"
VIDEO_DIR="$PROJECT_DIR/videos"

# Default values
HOURS=20
INTERVAL=15
OUTPUT_DIR="$IMG_DIR"
WIDTH=""
HEIGHT=""
ADD_TIMESTAMP=true  # Default to adding timestamp

# Parse optional arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --hours|-H)
      HOURS="$2"
      shift 2
      ;;
    --interval|-i)
      INTERVAL="$2"
      shift 2
      ;;
    --output-dir|-o)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    --width)
      WIDTH="$2"
      shift 2
      ;;
    --height)
      HEIGHT="$2"
      shift 2
      ;;
    --no-timestamp)
      ADD_TIMESTAMP=false
      shift
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--hours <hours>] [--interval <seconds>] [--output-dir <dir>] [--width <w>] [--height <h>] [--no-timestamp]"
      exit 1
      ;;
  esac
done

# Create necessary directories if they don't exist
mkdir -p "$OUTPUT_DIR"
mkdir -p "$VIDEO_DIR"

# Generate video filename at the start of the capture period.
# Format: YYYY_monDD.mp4 (e.g., 2024_jul18.mp4)
# Lowercase the entire filename for consistency (affects month abbr only).
VIDEO_FILENAME=$(date +%Y_%b%d.mp4 | tr '[:upper:]' '[:lower:]')
VIDEO_PATH="$VIDEO_DIR/$VIDEO_FILENAME"

# Check if output directory has existing images
RESUME=false
if [ -n "$(find "$OUTPUT_DIR" -maxdepth 1 -name "*.jpg" -type f 2>/dev/null)" ]; then
  echo "Found existing images in $OUTPUT_DIR"
  echo "Do you want to remove them and start fresh? (y/n)"
  read -r confirm
  if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
    rm -f "$OUTPUT_DIR"/*.jpg
    echo "Cleanup complete. Starting fresh capture."
  else
    echo "Continuing from last frame..."
    RESUME=true
  fi
fi

# Check if Python scripts exist
if [ ! -f "$PROJECT_DIR/capture_timelapse.py" ] || [ ! -f "$PROJECT_DIR/create_timelapse.py" ]; then
  echo "Error: Required Python scripts not found in $PROJECT_DIR."
  exit 1
fi

# Run the capture script with specified duration and interval.
echo "Starting ${HOURS}-hour timelapse capture with ${INTERVAL}-second interval..."
RESUME_FLAG=""
if [ "$RESUME" = true ]; then
  RESUME_FLAG="--resume"
fi
if [ "$ADD_TIMESTAMP" = true ]; then
  cd "$PROJECT_DIR" && uv run capture_timelapse.py --hours "$HOURS" --interval "$INTERVAL" --output-dir "$OUTPUT_DIR" --add-timestamp ${WIDTH:+--width "$WIDTH"} ${HEIGHT:+--height "$HEIGHT"} $RESUME_FLAG
else
  cd "$PROJECT_DIR" && uv run capture_timelapse.py --hours "$HOURS" --interval "$INTERVAL" --output-dir "$OUTPUT_DIR" ${WIDTH:+--width "$WIDTH"} ${HEIGHT:+--height "$HEIGHT"} $RESUME_FLAG
fi
echo "Timelapse capture finished."

# After capture is complete, create the video.
echo "Creating timelapse video: $VIDEO_PATH"
cd "$PROJECT_DIR" && uv run create_timelapse.py "$OUTPUT_DIR" "$VIDEO_PATH"

echo "Timelapse process completed successfully. Video saved to $VIDEO_PATH"

