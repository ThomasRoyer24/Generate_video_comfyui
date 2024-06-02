import API_create_image
import gpt_comfyui



data = gpt_comfyui.open_ai()
image_links=[]
if data !=0:

    
    for prompt in data:

        image_link = API_create_image.generate_image(prompt)
        image_links.append(image_link)

    print(image_links)



