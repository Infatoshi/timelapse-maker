from dataclasses import dataclass
from pathlib import Path
import argparse
import time
import cv2
from datetime import datetime
import re

@dataclass
class Resolution:
    width: int
    height: int

def add_timestamp(frame):
    # Get current local time in military format (HH:MM)
    now = datetime.now()
    time_str = now.strftime("%H:%M")

    # Set font properties (medium-small, white)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2.0
    font_thickness = 2
    color = (255, 255, 255)  # White

    # Get text size
    text_size = cv2.getTextSize(time_str, font, font_scale, font_thickness)[0]

    # Position: top-left with padding
    text_x = 20
    text_y = text_size[1] + 20

    # Put text on frame
    cv2.putText(frame, time_str, (text_x, text_y), font, font_scale, color, font_thickness)

    return frame

def find_last_frame_number(output_dir: Path) -> int:
    """Find the highest frame number in the output directory."""
    frame_files = list(output_dir.glob("frame_*.jpg"))
    if not frame_files:
        return 0
    
    max_frame = 0
    for frame_file in frame_files:
        # Extract frame number from filename (e.g., frame_0001.jpg -> 1)
        match = re.search(r'frame_(\d+)\.jpg', frame_file.name)
        if match:
            frame_num = int(match.group(1))
            max_frame = max(max_frame, frame_num)
    
    return max_frame

def capture_timelapse(
    duration: float,
    interval: int,
    output_dir: Path,
    use_timestamp: bool = True,
    resolution: Resolution = None,
    resume: bool = False,
):
    # Try different camera indices
    camera = None
    for i in range(10):
        test_camera = cv2.VideoCapture(0)
        if test_camera.isOpened():
            # Test if we can actually read from it
            ret, frame = test_camera.read()
            if ret and frame is not None:
                camera = test_camera
                print(f"Found working camera at index {i}")
                break
            else:
                test_camera.release()
        else:
            test_camera.release()
    
    if camera is None:
        raise RuntimeError("No working camera found. Please connect a camera device or use a test mode.")

    # Set resolution if specified
    if resolution:
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolution.width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution.height)

    # Get actual resolution
    width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Camera resolution: {width}x{height}")

    num_frames = int(duration // interval)
    
    # Determine starting frame number
    start_frame = 1
    if resume:
        last_frame = find_last_frame_number(output_dir)
        if last_frame > 0:
            start_frame = last_frame + 1
            print(f"Resuming from frame {start_frame} (found {last_frame} existing frames)")
        else:
            print("Resume requested but no existing frames found. Starting from frame 1.")

    try:
        for i in range(start_frame, start_frame + num_frames):
            # Capture frame
            ret, frame = camera.read()
            if not ret:
                print(f"Failed to capture frame {i}")
                continue

            # Add current timestamp to the frame if flag is True
            if use_timestamp:
                frame = add_timestamp(frame)

            filename = output_dir / f"frame_{i:04d}.jpg"
            cv2.imwrite(str(filename), frame)
            total_frames = start_frame + num_frames - 1
            print(f"Captured frame {i}/{total_frames}{' with timestamp' if use_timestamp else ''}")

            if i < start_frame + num_frames - 1:
                time.sleep(interval)

    except KeyboardInterrupt:
        print("\nCapture interrupted by user")
    finally:
        # Release the camera
        camera.release()
        print("Timelapse capture completed.")

def main():
    parser = argparse.ArgumentParser(
        description="Capture timelapse images using OpenCV."
    )
    parser.add_argument(
        "--hours",
        "-H",
        type=float,
        required=True,
        help="Duration of timelapse in hours",
    )
    parser.add_argument(
        "--interval",
        "-i",
        type=int,
        required=True,
        help="Interval between frames in seconds",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default="timelapse_images",
        help="Where to save the frames",
    )
    parser.add_argument(
        "--add-timestamp",
        action="store_true",
        default=True,
        help="Add military time timestamp to frames (default: True)",
    )
    parser.add_argument("--width", type=int, help="Custom width for capture")
    parser.add_argument("--height", type=int, help="Custom height for capture")
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from the last captured frame instead of starting fresh",
    )

    args = parser.parse_args()

    duration = 3600 * args.hours  # Total duration in seconds

    resolution = None
    if args.width and args.height:
        resolution = Resolution(args.width, args.height)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    capture_timelapse(
        duration=duration,
        interval=args.interval,
        output_dir=output_dir,
        use_timestamp=args.add_timestamp,
        resolution=resolution,
        resume=args.resume,
    )

if __name__ == "__main__":
    main()

