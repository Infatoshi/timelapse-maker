import os

import cv2


def create_timelapse_video(image_folder, output_video):
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    images.sort()

    # Get the dimensions of the first image
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(output_video, fourcc, 30, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

    print(f"Timelapse video saved as {output_video}")


if __name__ == "__main__":
    create_timelapse_video("./timelapse_images_4k", "timelapsed_imgs.mp4")
