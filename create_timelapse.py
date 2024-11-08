import os
import subprocess
import re

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
    create_timelapse_video("./timelapse_images", "timelapsed_imgs.mp4")
