import os
import time

import cv2


def capture_timelapse(duration, interval):
    # Create a directory to store the images
    if not os.path.exists("timelapse_images_4k"):
        os.makedirs("timelapse_images_4k")

    # Initialize the camera
    cap = cv2.VideoCapture(0)

    # Set the resolution to 4K (3840x2160)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

    # Force MJPG format for better compatibility with high resolutions
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))

    # Verify the settings
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Camera resolution set to: {width}x{height}")

    # Calculate the number of frames to capture
    num_frames = int(duration / interval)

    for i in range(num_frames):
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret:
            # Save the frame as an image
            cv2.imwrite(f"timelapse_images_4k/frame_{i:04d}.jpg", frame)
            print(f"Captured frame {i+1}/{num_frames}")
        else:
            print(f"Failed to capture frame {i+1}")

        # Wait for the specified interval
        time.sleep(interval)

    # Release the camera
    cap.release()


# Example usage
hours = 15
duration = 3600 * hours  # Total duration in seconds
interval = 15  # Interval between frames in seconds

capture_timelapse(duration, interval)
