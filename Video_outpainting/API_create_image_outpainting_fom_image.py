from urllib import request, parse
import random
import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
import os



server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())


def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
        else:
            continue #previews are binary data

    history = get_history(prompt_id)[prompt_id]
    return history["outputs"]["484"]["images"][0]["filename"] # print history to find the filename



def generate_image_outpainting(image_link,user_name,timestamp,model = "DreamShaperXL_Lightning.safetensors"):

    #Load workflow
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workflow_json = os.path.join(script_dir, 'workflow_outpainting_image.json')

    with open(workflow_json, "r", encoding="utf-8") as fichier:
        comfy_json = json.load(fichier)
        
    #Set the image in the workflow
    while comfy_json['492']['inputs']['image'] != image_link:
        comfy_json['492']['inputs']['image'] = image_link
    
    
    comfy_json['1']['inputs']['seed'] = random.randint(1, 999999999999)

    comfy_json['17']['inputs']['ckpt_name'] = model

    #Set output path
    comfy_json['484']['inputs']['filename_prefix'] = user_name+"/"+str(timestamp)+"/"+"Comfyui"

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    images = get_images(ws, comfy_json)
    return images


if __name__ == "__main__":
    
    generate_image_outpainting("0902.png","test","1234", "darksun_v41.safetensors")