from fastapi import FastAPI, UploadFile,File,Form
import uvicorn
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from tempfile import NamedTemporaryFile
import os
import cv2
from tensorflow import keras 
from keras.utils import img_to_array


from PIL import Image
import numpy as np
import base64
import requests
import io
import random
import shutil
import sys





app=FastAPI(title="Animating Video Using Stable Diffusion")

url="http://0.0.0.0:7860"

def animatingVideos(input_video_path,prompt,negative_prompt,ml_model):

    output_frame_path="/home/cs-ai-09/Group 8 DS Project/Files/Project-8-DS-MACE--master/Result Frames/Sample"
    shutil.rmtree(output_frame_path, ignore_errors=True, onerror=lambda _, __, ___: None)
    if not os.path.exists(output_frame_path):
        os.makedirs(output_frame_path)
    #Capturing frames from video
    cap = cv2.VideoCapture(input_video_path)

    BASEDIR=os.path.dirname(os.path.abspath(__file__))
    OUTPUT_FOLDER=os.path.join(BASEDIR,"Output")
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    output_video_path=os.path.join(OUTPUT_FOLDER,"sample.mp4")

    if not cap.isOpened():
        print("Error: Unable to open the video file.")
        return "Failed"

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
    sampling_step=20
    for frame_number in range(total_frames):
        ret, frame = cap.read()
        
        sys.stdout.write('\r\r' +"LOADING: "+ symbols[index]+" "+str(int((frame_number/total_frames)*100))+" %")
        sys.stdout.flush()

        index = (index + 1) % len(symbols)
        if frame_number==0:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = cv2.resize(rgb_image, (256, 256))
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array /= 255.
            predictions = ml_model.predict(img_array)
            predicted_class = np.argmax(predictions[0])
            class_labels = {'20': 0, '30': 1, '40': 2, '50': 3}
            class_labels = {v: k for k, v in class_labels.items()}
            sampling_step = class_labels[predicted_class]
            print(f'Predicted No. of. Sampling Steps for this video: {sampling_step}')
        if frame_number%2==1:
            video.write(bgr_image)
            continue

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
        "steps": sampling_step,
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
        
        frame_filename = os.path.join(output_frame_path, f"frame_{frame_number:04d}.jpg")
        animated_image.save(frame_filename) 
        image_array=np.array(animated_image)
        bgr_image=cv2.cvtColor(image_array,cv2.COLOR_BGR2RGB)
        video.write(bgr_image)
    video.release()
    print("\nVideo created at: "+output_video_path)
    return output_video_path












@app.get('/')
def root():
    return {'message':"Hello World"}

@app.post("/AnimateVideo")
def file_upload(prompt:str=Form(...),negative_prompt:str=Form(...),files:UploadFile=File(...)):
    temp_input = NamedTemporaryFile(delete=False)
    model_path = "/home/cs-ai-09/Group 8 DS Project/Files/FastAPI/CNN_Model/new_model3.h5"
    model = keras.models.load_model(model_path)
    if files.content_type!="video/mp4":
        raise HTTPException(400,detail="Invalid Video Type")
    # try:
    # try:
    data=files.file.read()
    with temp_input as f:
        f.write(data)
        
    # except Exception as E:
    #     return {"message":E}
    # finally:
    #     files.file.close()
    output_path=animatingVideos(temp_input.name,
                                    prompt,
                                    negative_prompt,
                                    model)
    # except Exception as E:
    #     return {"message":E}
    # finally:
    #     os.remove(temp_input.name)

    return FileResponse(path=output_path,media_type="application/octet-stream",filename="sample.mp4")





if __name__=='__main__':
    uvicorn.run(app,port=52087)
