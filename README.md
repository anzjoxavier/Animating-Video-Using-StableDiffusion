# Animating Videos Using Stable Diffusion

> B.Tech final year project done by [Anz Jo Xavier](https://www.linkedin.com/in/anzjox/), [Nidheesh S](https://www.linkedin.com/in/nidheesh-s-47a575210/) and [Yedhu Krishnan PG](https://www.linkedin.com/in/yedhu-krishnan-p-g-495aa8234/).

- Converts a raw video into animation
- Video is sliced into frames first
- Uses Stable diffusion to convert frames to animation
- Animated frames are joined together to make animated video
- Used Controlnet in stable diffusion to track movements
- Trained a CNN Model to predict parameters for Stable diffusion considering the quality of video
- Made a FastAPI Server for easy usage

# Result
### Input Video
<img src="https://github.com/anzjoxavier/Project-Group-8-DS-MACE/assets/116029351/4ebb50e8-afd0-4072-bc76-bf08927ada39" width="250" height="250"/>

### Output Video

<img src="https://github.com/anzjoxavier/Project-Group-8-DS-MACE/assets/116029351/18a99ba7-6a6d-4d16-ad79-6e9d45741d19" width="250" height="250"/>



> [!TIP]
> Checkpoint Used in Stable Diffusion: aniverse_V13.safetensors [9fe4fec28d]


> [!NOTE]
> Usage of above server requires Stable diffusion Automatic1111 preinstalled in your PC.
