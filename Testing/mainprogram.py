import cv2
from PIL import Image
import numpy as np
import base64
import requests
import io
import os
import random
import shutil
import sys

url="http://0.0.0.0:7860"

def animatingVideos(input_video_path,output_video_path,prompt,negative_prompt):

    output_folder="/home/cs-ai-09/Group 8 DS Project/Files/Project-8-DS-MACE--master/Result Frames/Sample"
    shutil.rmtree(output_folder, ignore_errors=True, onerror=lambda _, __, ___: None)

    #Capturing frames from video
    cap = cv2.VideoCapture(input_video_path)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if not cap.isOpened():
        print("Error: Unable to open the video file.")

    #Printing fps and frames
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Video FPS: {fps}")
    print(f"Total Frames: {total_frames}")

    symbols = ['-', '\\', '|', '/']
    index = 0

    #Generating Seed
    seed = random.randint(10**9, 10**10 - 1)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v") 
    video = cv2.VideoWriter(output_video_path, fourcc, 30, (512, 512))

    for frame_number in range(total_frames):
        ret, frame = cap.read()
        
        sys.stdout.write('\r\r' +"LOADING: "+ symbols[index]+" "+str(int((frame_number/total_frames)*100))+" %")
        sys.stdout.flush()

        index = (index + 1) % len(symbols)

        if not ret:
            print(f"Error reading frame {frame_number}")
            break
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR), 'RGB')
        with io.BytesIO() as output:
            image.save(output,format="PNG")
            image_bytes=output.getvalue()
        image_encode=base64.b64encode(image_bytes).decode('utf-8')
        
        img2img_data={
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "seed": seed,
        "steps": 40,
        "cfg_scale": 7,
        "width": 512,
        "height": 512,
        "sampler_name": "DPM++ 2M Karras",
        "sd_model_name": "aniverse_V13.safetensors [9fe4fec28d]",
        "sd_model_hash": "d6548414b4",
        "denoising_strength": 0.75,
        "comments": {},
        "init_images": [
        image_encode
        ],
        "alwayson_scripts": {
            "controlnet":{
                "args":[
                    {   "input_image":image_encode,
                        "pixel_perfect":True,
                        "module":"lineart_standard (from white bg & black line)",
                        "model":"control_v11p_sd15s2_lineart_anime [3825e83e]",
                        "Control Mode": "ControlNet is more important"
                    },
                    {   "input_image":image_encode,
                        "pixel_perfect":True,
                        "module":"canny",
                        "model":"control_v11p_sd15_canny [d14c016b]",
                        "Control Mode": "ControlNet is more important"
                    },
                    {   "input_image":image_encode,
                        "pixel_perfect":True,
                        "module":"openpose_full",
                        "model":"control_v11p_sd15_openpose [cab727d4]",
                        "Control Mode": "ControlNet is more important"
                    }
                ]
            }
        }

        }
        response=requests.post(url=f"{url}/sdapi/v1/img2img",json=img2img_data).json()['images'][0]
        animated_image=Image.open(io.BytesIO(base64.b64decode(response)))
        
        frame_filename = os.path.join(output_folder, f"frame_{frame_number:04d}.jpg")
        animated_image.save(frame_filename) 
        image_array=np.array(animated_image)
        bgr_image=cv2.cvtColor(image_array,cv2.COLOR_BGR2RGB)
        video.write(bgr_image)
    video.release()
    print("\nVideo created at: "+output_video_path)


if __name__ == "__main__":
    video_path="/home/cs-ai-09/Group 8 DS Project/Files/Project-8-DS-MACE--master/Input Videos/child_guitar.mp4"
    output_path="/home/cs-ai-09/Group 8 DS Project/Files/Project-8-DS-MACE--master/output_Athlete_running.mp4"
    prompt="animate the picture, in style of a Pixer 3D rendered cartoon, exaggerated features, simple flat white background,good quality, high quality"
    negative_prompt="low quality, worst quality"
    animatingVideos(video_path,output_path,prompt,negative_prompt)

