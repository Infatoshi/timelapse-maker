from datetime import datetime, timedelta

import cv2


def add_timestamp(frame, timestamp):
    # Convert timestamp to string format
    time_str = timestamp.strftime("%I:%M %p")

    # Get frame dimensions
    height, width = frame.shape[:2]

    # Set font properties
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    font_thickness = 2
    color = (255, 255, 255)  # White color

    # Get text size
    text_size = cv2.getTextSize(time_str, font, font_scale, font_thickness)[0]

    # Calculate position (top right corner with some padding)
    text_x = width - text_size[0] - 20
    text_y = text_size[1] + 20

    # Put text on frame
    cv2.putText(
        frame, time_str, (text_x, text_y), font, font_scale, color, font_thickness
    )

    return frame


# Open the input video
input_video = cv2.VideoCapture("timelapsed_imgs.mp4")

# Check if video opened successfully
if not input_video.isOpened():
    print("Error: Could not open video file. Please check the file path and format.")
    exit()

# Get video properties
fps = int(input_video.get(cv2.CAP_PROP_FPS))
width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))

# Check if we got valid video properties
if fps <= 0 or width <= 0 or height <= 0 or total_frames <= 0:
    print("Error: Invalid video properties. Please check the video file.")
    exit()

# Create VideoWriter object for output video
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
output_video = cv2.VideoWriter("output_timelapse.mp4", fourcc, fps, (width, height))

# Calculate time per frame
start_time = datetime(2023, 1, 1, 20, 0)  # Start at 11:00 PM
end_time = datetime(2023, 1, 2, 16, 0)  # End at 6:00 AM next day
total_duration = (end_time - start_time).total_seconds()

# Avoid division by zero
if total_frames > 0:
    time_per_frame = total_duration / total_frames
else:
    print("Error: Video has no frames.")
    exit()

frame_count = 0
while True:
    ret, frame = input_video.read()
    if not ret:
        break

    # Calculate current timestamp
    current_time = start_time + timedelta(seconds=frame_count * time_per_frame)

    # Add timestamp to frame
    frame_with_timestamp = add_timestamp(frame, current_time)

    # Write frame to output video
    output_video.write(frame_with_timestamp)

    frame_count += 1

# Release video objects
input_video.release()
output_video.release()

print(
    f"Processing complete. Output saved as 'output_timelapse.mp4'. Processed {frame_count} frames."
)
