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

https://github.com/anzjoxavier/Project-Group-8-DS-MACE/assets/116029351/b40e254b-7f7b-40e4-94cc-d1147543d642

### Output Video

https://github.com/anzjoxavier/Project-Group-8-DS-MACE/assets/116029351/9d980df7-7a1f-4629-a389-d28596a935ae

> [!TIP]
> Checkpoint Used in Stable Diffusion: aniverse_V13.safetensors [9fe4fec28d]


> [!NOTE]
> Usage of above server requires Stable diffusion Automatic1111 preinstalled in your PC.
