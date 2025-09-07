import os
import subprocess
import re
import argparse

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

def create_timelapse_video(image_folder, output_video):
    # Get all jpg files and sort them naturally
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    images.sort(key=natural_sort_key)

    # Create a text file with the correct order of frames
    with open('frames.txt', 'w') as f:
        for img in images:
            f.write(f"file '{os.path.join(image_folder, img)}'\n")

    # Use the text file as input for ffmpeg
    subprocess.run([
        "ffmpeg",
        "-y",  # Overwrite output file if it exists
        "-f", "concat",
        "-safe", "0",
        "-i", "frames.txt",
        "-framerate", "30",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "ultrafast",
        output_video
    ])

    # Clean up the temporary file
    os.remove('frames.txt')

    print(f"Timelapse video saved as {output_video}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a timelapse video from a folder of images.")
    parser.add_argument("image_folder", help="Path to the folder containing images.")
    parser.add_argument("output_video", help="Path to the output video file.")
    args = parser.parse_args()

    create_timelapse_video(args.image_folder, args.output_video)

