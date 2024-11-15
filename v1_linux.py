import argparse
import os
import time
import subprocess
from datetime import datetime

def capture_timelapse(duration, interval):
    # Create a directory to store the images
    output_folder = "timelapse_images"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Calculate the number of frames to capture
    num_frames = int(duration / interval)

    for i in range(num_frames):
        # Generate the filename with a timestamp
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_folder}/frame_{i}.jpg"

        # Capture the image using fswebcam
        subprocess.run(["fswebcam", "-r", "1920x1080", "--no-banner", filename])

        print(f"Captured frame {i+1}/{num_frames}")

        # Wait for the specified interval
        time.sleep(interval)

    print("Timelapse capture completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture timelapse images.")
    parser.add_argument("--hours", type=float, required=True, help="Duration of timelapse in hours")
    parser.add_argument("--interval", type=int, required=True, help="Interval between frames in seconds")
    
    args = parser.parse_args()
    
    duration = 3600 * args.hours  # Total duration in seconds
    interval = args.interval  # Interval between frames in seconds

    capture_timelapse(duration, interval)
