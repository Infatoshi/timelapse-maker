import argparse
import os
import time
import cv2
from datetime import datetime

def capture_timelapse(duration, interval, device=0, resolution=None):
    """
    Capture timelapse using OpenCV
    
    Args:
        duration (float): Duration in seconds
        interval (int): Interval between frames in seconds
        device (int): Camera device index
        resolution (tuple): Optional (width, height) tuple for resolution
    """
    # Create a directory to store the images
    output_folder = "timelapse_images"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Calculate the number of frames to capture
    num_frames = int(duration / interval)

    # Initialize camera
    cap = cv2.VideoCapture(device)
    
    if not cap.isOpened():
        print(f"Error: Could not open camera {device}")
        return

    # Set resolution if specified
    if resolution:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    # Get actual camera properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Camera resolution: {width}x{height}")

    try:
        for i in range(num_frames):
            # Capture frame
            ret, frame = cap.read()
            
            if not ret:
                print(f"Error capturing frame {i+1}")
                continue

            # Generate the filename
            filename = f"{output_folder}/frame_{i:04d}.jpg"
            
            # Save the image
            cv2.imwrite(filename, frame)
            print(f"Captured frame {i+1}/{num_frames}")

            # Wait for the specified interval
            if i < num_frames - 1:  # Don't wait after the last frame
                time.sleep(interval)

    except KeyboardInterrupt:
        print("\nCapture interrupted by user")
    finally:
        # Release the camera
        cap.release()
        print("Timelapse capture completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture timelapse images using OpenCV.")
    parser.add_argument("--hours", type=float, help="Duration of timelapse in hours")
    parser.add_argument("--interval", type=int, help="Interval between frames in seconds")
    parser.add_argument("--width", type=int, help="Custom width for capture")
    parser.add_argument("--height", type=int, help="Custom height for capture")
    
    args = parser.parse_args()

    # If hours and interval weren't provided as arguments, ask for them now
    if args.hours is None:
        while True:
            try:
                hours = float(input("Enter duration in hours: "))
                if hours > 0:
                    break
                print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")
    else:
        hours = args.hours

    if args.interval is None:
        while True:
            try:
                interval = int(input("Enter interval between frames in seconds: "))
                if interval > 0:
                    break
                print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")
    else:
        interval = args.interval

    duration = 3600 * hours  # Total duration in seconds
    
    # Set resolution if both width and height are provided
    resolution = None
    if args.width and args.height:
        resolution = (args.width, args.height)

    capture_timelapse(duration, interval, 0, resolution)
