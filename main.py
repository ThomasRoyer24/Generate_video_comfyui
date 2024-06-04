import API_create_image
import API_create_video
import gpt_comfyui



data = gpt_comfyui.open_ai()
image_links=[]
if data !=0:

    
    for prompt in data:

        image_link = API_create_image.generate_image(prompt,"test")
        image_links.append(image_link)

    video_link = API_create_video.generate_video(image_links,"test",2)



