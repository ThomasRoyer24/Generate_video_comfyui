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
    output_images = {}
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
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = image['filename']
                    images_output.append(image_data)
            output_images[node_id] = images_output

    return output_images


def generate_image(prompt):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    workflow_json = os.path.join(script_dir, 'v1.json')

    with open(workflow_json, "r", encoding="utf-8") as fichier:
        comfy_json = json.load(fichier)
    print(comfy_json)
        
    comfy_json['3']['inputs']['seed'] = random.randint(1, 999999999999)
    comfy_json['6']['inputs']['text'] = prompt

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    images = get_images(ws, comfy_json)
    return images['9'][0]


def generate_video(image_link,user_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workflow_json = os.path.join(script_dir, 'workflow_video_test.json')

    with open(workflow_json, "r+", encoding="utf-8") as fichier:
        base_json = fichier.read()

    num_image = len(image_link)
    for i in range(num_image):
        
        #Add IPAdapter Batch
        base_json += ',"{}":'.format(i)
        base_json += ' {"inputs": {"weight": 1,"weight_type": "ease in-out","start_at": 0,"end_at": 1,"embeds_scaling": "V only","encode_batch_size": 0,"model": ["573",0],"ipadapter": ["573",1],"image": ["683",0],"attn_mask": ["713",0]},"class_type": "IPAdapterBatch","_meta": {"title": "IPAdapter Batch (Adv.)"}}'
        
        #Mask
        base_json += ',"{}":'.format(i + 10)
        base_json += ' {"inputs": {"points_string": "","invert": false,"frames": 96,"width": 512,"height": 512,"interpolation": "linear"},"class_type": "CreateFadeMaskAdvanced","_meta": {"title": "Create Fade Mask Advanced"}}'
        
        #Load image
        base_json += ',"{}":'.format(i + 20)
        base_json +=' {"inputs": {"image": "","upload": "image"},"class_type": "LoadImage","_meta": {"title":"Load Image"}}'
        
    base_json += "}"
    
    comfy_json = json.loads(base_json)

    for i, link in enumerate(image_link):
        comfy_json[str(20+i)]['inputs']['image'] = "D:/ComfyUi/ComfyUI_windows_portable/ComfyUI/output/"+user_name+"/"+link
    print(comfy_json[str(20+i)])


generate_video(["ComfyUI_00005_"],"test")

def test(prompt):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workflow_json = os.path.join(script_dir, 'v1.json')

    with open(workflow_json, "r+", encoding="utf-8") as fichier:
        text = fichier.read()
    text += '"9": {"class_type": "SaveImage","inputs": {"filename_prefix": "test/ComfyUI","images": ["8",0]}}}'
    
    comfy_json = json.loads(text)

    comfy_json['3']['inputs']['seed'] = random.randint(1, 999999999999)
    comfy_json['6']['inputs']['text'] = prompt

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    images = get_images(ws, comfy_json)
    return images['9'][0]


"""
,"682": {"inputs": {"weight": 1,"weight_type": "ease in-out","start_at": 0,"end_at": 1,"embeds_scaling": "V only","encode_batch_size": 0,"model": ["573",0],"ipadapter": ["573",1],"image": ["683",0],"attn_mask": ["713",0]},"class_type": "IPAdapterBatch","_meta": {"title": "IPAdapter Batch (Adv.)"}}


,"701": {"inputs": {"points_string": "0:(1.0),\n40:(1.0),\n48:(0.0),\n88:(0.0),\n96:(1.0)","invert": false,"frames": 96,"width": 512,"height": 512,"interpolation": "linear"},"class_type": "CreateFadeMaskAdvanced","_meta": {"title": "Create Fade Mask Advanced"}}

,"142": {"inputs": {"image": "reference-1.jpeg","upload": "image"},"class_type": "LoadImage","_meta": {"title":"Load Image"}}"""