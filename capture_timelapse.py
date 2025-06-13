import argparse
from dataclasses import dataclass
from pathlib import Path
import platform
import time
import subprocess


@dataclass
class Resolution:
    width: int
    height: int


def capture_timelapse_opencv(
    duration: float,
    interval: int,
    output_dir: Path,
    device: int = 0,
    resolution: Resolution = None,
):
    import cv2

    # Initialize camera
    cap = cv2.VideoCapture(device)

    if not cap.isOpened():
        print(f"Error: Could not open camera {device}")
        return

    # Set resolution if specified
    if resolution:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution.height)

    # Get actual camera properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Camera resolution: {width}x{height}")

    num_frames = int(duration // interval)

    try:
        for i in range(1, num_frames + 1):
            ret, frame = cap.read()

            if not ret:
                print(f"Error capturing frame {i+1}")
                continue

            filename = output_dir / f"frame_{i:04d}.jpg"

            cv2.imwrite(filename, frame)
            print(f"Captured frame {i}/{num_frames}")

            if i < num_frames:
                time.sleep(interval)

    except KeyboardInterrupt:
        print("\nCapture interrupted by user")
    finally:
        # Release the camera
        cap.release()
        print("Timelapse capture completed.")


def capture_timelapse_linux(
    duration: float,
    interval: int,
    output_dir: Path,
    resolution: Resolution = None,
    device: int = 0,
):
    num_frames = int(duration // interval)

    for i in range(1, num_frames + 1):
        filename = f"{output_dir}/frame_{i:04d}.jpg"

        # Capture the image using fswebcam
        subprocess.run(["fswebcam", "-r", "1920x1080", "--no-banner", filename])

        print(f"Captured frame {i}/{num_frames}")

        if i < num_frames:
            time.sleep(interval)

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
    parser.add_argument("--width", type=int, help="Custom width for capture")
    parser.add_argument("--height", type=int, help="Custom height for capture")

    args = parser.parse_args()

    duration = 3600 * args.hours  # Total duration in seconds

    resolution = None
    if args.width and args.height:
        resolution = Resolution(args.width, args.height)

    mapping = {
        "Linux": capture_timelapse_linux,
        "Darwin": capture_timelapse_opencv,
        "Windows": capture_timelapse_opencv,
    }

    os_type = platform.system()
    try:
        capture_timelapse = mapping[os_type]
    except KeyboardInterrupt:
        parser.error(f"Unsupported OS: {os_type}")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    capture_timelapse(
        duration=duration,
        interval=args.interval,
        output_dir=output_dir,
        resolution=resolution,
        device=0,
    )


if __name__ == "__main__":
    main()
