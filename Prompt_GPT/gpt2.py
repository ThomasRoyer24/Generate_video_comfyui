import requests
import json

def open_ai(text_to_decribe,global_texte,Charactere_information):

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
        "messages": [
            {
                "role": "system",
                "content": 'You are an AI assistant that creates high-quality, coherent Stable Diffusion prompts based on user input. You will receive 3 texts, text_to_decribe: which is the paragraph you have to process and global_texte: which is the general text including text_to_decribe. global_texte is just to help you better understand text_to_decribe which is the text to process. The last text is Charactere_information which contains information on the different characters to use in case the characters are present in text_to_decribe. .Focus on describing the most important aspects of the scene, such as character position, movement, background, environment, action, lighting, composition, pose, and location and specify camera movement. Use keywords that are coherent with the input theme. You can include explanations or additional information that matches the context of the story. Structure your response as a numbered list of prompts, with one prompt per line., rules: Analyze the user input carefully to identify the key elements and theme.,Generate concise, descriptive prompts that capture the essence of the scene., Ensure each prompt is coherent and relevant to the input theme., Include essential details such as gender, camera movement, and scene composition., Present the prompts as a numbered list, with one prompt per line and no additional information. examples:  input: A group of friends enjoying a picnic in a sunny park., output:  1. Group of diverse friends laughing and chatting, sitting on colorful picnic blankets, park background, sunny day, wide angle, 2. Close-up of hands reaching for various foods and drinks on the picnic blanket, shallow depth of field, 3. Two friends playing frisbee in the background, motion blur, park setting, vibrant colors, medium shot, 4. Sun flare through trees, silhouette of friends raising glasses for a toast, backlit, warm tones, close-up, 5. Aerial view of the picnic scene, friends laying on blankets forming a circular pattern, park landscape, bright daylight. You only have to generate the prompt for text_to_decribe'

            },
            {
                "role": "user",
                "content": "text_to_decribe :"+ text_to_decribe + ". global_texte :" + global_texte + ". Charactere_information :" + Charactere_information
            }
        ]
        
    }

    response = requests.post(url, headers=headers, json=data)

    print(response)
    if response.status_code == 200:

        data = response.json()['choices'][0]['message']['content']

        print(data)
    else:
        print("Error:", response.status_code, response.text)
        return 0


global_t = "On a golden beach, a woman named Lily was enjoying her solitude. The sun was warm, the waves were gentle, and the sand was soft under her feet. Suddenly, she stumbled upon a bottle half-buried in the sand. Inside, a map with cryptic symbols and a path leading to a hidden treasure. Intrigued, Lily decided to follow the map. She journeyed through the beach, uncovering clues hidden in the sand, rocks, and even the waves. Each clue brought her closer to the treasure, her heart pounding with anticipation. As the sun began to set, painting the sky with hues of orange and pink, Lily reached the final spot. She dug into the sand and found an ancient chest. With bated breath, she opened it, only to find it filled with old books and scrolls. Disappointed at first, Lily soon realized that the books were filled with wisdom and knowledge from centuries ago. She spent the rest of the evening engrossed in the books, learning about the world, life, and herself. As the moon rose, Lily sat there on the beach, the chest of wisdom by her side. She realized that the true treasure was not gold or jewels, but the journey she had embarked on and the wisdom she had gained. And with that, she smiled, content in her heart."

v = "On a golden beach, a woman named Lily was enjoying her solitude. The sun was warm, the waves were gentle, and the sand was soft under her feet."

t = "characters: name: Lily, description: clothing: casual beach attire, hair_color: unspecified, eye_color: unspecified, jewelry_accessories: no jewelry, other_details: enjoying solitude on a golden beach."

open_ai(t,global_t,v)