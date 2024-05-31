import requests
import json

def open_ai():
    openai_api_key = 'sk-proj-pxTJRnvjYbD3ZnMODD4bT3BlbkFJ9jz0zuOcmc42jGymPMUT'
    if openai_api_key is None:
        raise ValueError("OpenAI API key is not set in environment variables.")

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "system",
                "content": "Given the following story, return a JSON object representing a series of 'images' from the story. Each image should encapsulate a distinct scene or moment from the story. There is no limit to the number of images, but ensure each image includes a detailed description that covers the following elements: character clothing and color, hair color, eye color, jewelry and/or accessories, character position, movement, background, environment, action, lighting, composition, pose, location, and particles in the air. Each image should be represented as 'image1', 'image2', etc. in the JSON object."

            },
            {
                "role": "user",
                "content": "Marie was strolling through the park, the sun gently declining on the horizon. The trees around her were in full bloom, their pink and white petals forming a delicate carpet on the path. She paused for a moment to listen to the melodious birdsong, a smile of serenity on her face. A small squirrel approached, curious, and she handed it a nut from her bag. Continuing her walk, she came across an elderly couple hand in hand, their love palpable in their knowing glances. In the distance, the laughter of children at play mingled with the sound of the central fountain. Marie felt invaded by a sense of peace, savoring every moment of this stroll. She sat down on a bench, closing her eyes to enjoy the light, fragrant breeze."
            }
        ]
        
    }

    response = requests.post(url, headers=headers, json=data)

    
    if response.status_code == 200:
    #    print("Response from OpenAI:", response.json())
    #    print('\n')

        data = response.json()['choices'][0]['message']['content']
        data = json.loads(data)

        prompt_list =[]
        for image_key, image_value in data.items():
            prompt_list.append(extract_values(image_value))
        return prompt_list

    else:
        print("Error:", response.status_code, response.text)
        return 0




def extract_values(image):
    return ', '.join(image.values())
