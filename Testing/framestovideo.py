import cv2
import os

def frames_to_video(input_folder, output_video_path, output_fps):
    # Get the list of image files in the input folder
    images = [img for img in os.listdir(input_folder) if img.endswith(".png")]
    # Sort the images based on their numerical order in the filename
    images.sort()
    print(images)
    # Get the first image to retrieve the size information
    first_image = cv2.imread(os.path.join(input_folder, images[0]))
    height, width, layers = first_image.shape

    # Define the video codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # You can use other codecs like "XVID" or "MJPG"
    video = cv2.VideoWriter(output_video_path, fourcc, output_fps, (width, height))

    # Add each image to the video
    for image in images:
        img_path = os.path.join(input_folder, image)
        frame = cv2.imread(img_path)
        video.write(frame)

    # Release the video writer object
    video.release()

    print(f"Video created: {output_video_path}")

if __name__ == "__main__":
    input_folder = "/home/cs-ai-09/Group 8 DS Project/Files/Result Animated Frames/BoyGirlDancing"       # Replace with the folder containing your frames
    output_video_path = "output_video3.mp4"  # Replace with the desired output video path
    output_fps =20                        # Replace with your desired frames per second

    frames_to_video(input_folder, output_video_path, output_fps)

