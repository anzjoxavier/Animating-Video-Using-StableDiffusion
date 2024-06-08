import cv2
import os

def extract_frames(video_path, output_folder):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video opened successfully
    if not cap.isOpened():
        print("Error: Unable to open the video file.")
        return

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"Video FPS: {fps}")
    print(f"Total Frames: {total_frames}")

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through each frame and save it as an image
    for frame_number in range(total_frames):
        ret, frame = cap.read()

        if not ret:
            print(f"Error reading frame {frame_number}")
            break

        # Save the frame as an image
        frame_filename = os.path.join(output_folder, f"frame_{frame_number:04d}.jpg")
        cv2.imwrite(frame_filename, frame)

    # Release the video capture object
    cap.release()

    print("Frames extraction completed.")

# Example usage
video_path = "/home/cs-ai-09/Group 8 DS Project/Files/Input Videos/Dance.mp4"
output_folder = "/home/cs-ai-09/Group 8 DS Project/Files/Final Result/Dance.mp4"

extract_frames(video_path, output_folder)
