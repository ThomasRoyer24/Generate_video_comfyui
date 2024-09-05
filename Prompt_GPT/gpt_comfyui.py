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
                "content": 'Analyzing the input text to create "images" from the story. Each image should represent a major change in action, event, or any significant element of the story. For each image, describe the most important aspects of the scene, such as character position, movement, background, environment, action, lighting, composition, pose, and location, specifying camera movement. Use keywords coherent with the input theme. Include explanations or additional information that match the context of the story. Structure the response as a numbered list of prompts, with one prompt per line and no additional information. Follow these rules: analyze the user input carefully to identify the key elements and theme, generate concise and descriptive prompts capturing the essence of the scene, ensure each prompt is coherent and relevant to the input theme, include essential details such as gender, camera movement, and scene composition, and present the prompts as a numbered list, with one prompt per line and no additional information. Additionally, identify the different characters. For each character, provide a detailed description based on the text. If the text does not give specific indications, invent the descriptions while ensuring they match the context of the story. Describe character details including clothing (color, types of clothing), hair color and hairstyle, eye color, accessories, jewelry, and various elements to add interesting details. Return in JSON like charactere : clothing,hairstyle, hair color, eye color jewelry ... image1 : ... image2:...'

            },
            {
                "role": "user",
                "content": "On a golden beach, a woman named Lily was enjoying her solitude. The sun was warm, the waves were gentle, and the sand was soft under her feet. Suddenly, she stumbled upon a bottle half-buried in the sand. Inside, a map with cryptic symbols and a path leading to a hidden treasure. Intrigued, Lily decided to follow the map. She journeyed through the beach, uncovering clues hidden in the sand, rocks, and even the waves. Each clue brought her closer to the treasure, her heart pounding with anticipation. As the sun began to set, painting the sky with hues of orange and pink, Lily reached the final spot. She dug into the sand and found an ancient chest. With bated breath, she opened it, only to find it filled with old books and scrolls. Disappointed at first, Lily soon realized that the books were filled with wisdom and knowledge from centuries ago. She spent the rest of the evening engrossed in the books, learning about the world, life, and herself. As the moon rose, Lily sat there on the beach, the chest of wisdom by her side. She realized that the true treasure was not gold or jewels, but the journey she had embarked on and the wisdom she had gained. And with that, she smiled, content in her heart."
            }
        ]
        
    }

    response = requests.post(url, headers=headers, json=data)

    
    if response.status_code == 200:

        data = response.json()['choices'][0]['message']['content']
        data = json.loads(data)
        return data
        
"""
        prompt_list =[]
        for image_key, image_value in data.items():
            prompt_list.append(extract_values(image_value))
        
        return prompt_list

    else:
        print("Error:", response.status_code, response.text)
        return 0




def extract_values(image):
    return ', '.join(image.values())
"""


if __name__ == "__main__":
    print(open_ai())