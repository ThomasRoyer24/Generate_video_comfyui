from urllib import request, parse
import random
import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
import os
import time
import math
from Comfy_node_data import Comfy_node

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

def get_video(ws, prompt):
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


    return history["outputs"]["5"]["gifs"][0]["filename"] # print history to find the filename


def generate_video(image_link,duration,user_name,timestamp,musique_param=False,motion_component_param=False,motion_preset_param=False,effect=False,effect_param=False,model="depth_anything_v2_vits_fp32.safetensors"):

    #load workflow in text
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workflow_json = os.path.join(script_dir, 'depth_motions.json')

    with open(workflow_json, "r+", encoding="utf-8") as fichier:
        base_json = fichier.read()

    # modifier le fichier json pour le workflow    
    if motion_component_param:
        base_json += Comfy_node[motion_component_param[0][1]] # Pour acceder a la 2 eme valeur du premier tuple 

    if motion_preset_param:
        base_json += Comfy_node[motion_preset_param[0][1]] # Pour acceder a la 2 eme valeur du premier tuple 

    if effect:
        base_json += Comfy_node[effect]

    if musique_param:
        base_json += Comfy_node["Musique"]        

    base_json += "}" # close 


    #load update workflow in json
    comfy_json = json.loads(base_json)

    comfy_json["50"]["inputs"]["image"] = image_link
    comfy_json["109"]["inputs"]["value"] = duration
    comfy_json["86"]["inputs"]["model"] = model


    # Set param in motion 
    if motion_component_param:
        for param_name, param_value in motion_component_param:
            comfy_json["2"]["inputs"][param_name] = param_value

    if motion_preset_param:
        for param_name, param_value in motion_preset_param:
            comfy_json["1"]["inputs"][param_name] = param_value
        
    if effect_param:
        for param_name, param_value in effect_param:
            comfy_json["3"]["inputs"][param_name] = param_value
    
    if musique_param:
        comfy_json["204"]["inputs"]["audio"]= musique_param["musique_link"]
        comfy_json["204"]["inputs"]["start_time"]= musique_param["start_time"]
        comfy_json["204"]["inputs"]["duration"]= duration
        comfy_json["207"]["inputs"]["amount"]= duration*30 #30 frames/sec


    #Set connection nodes
    if motion_component_param:
        comfy_json["91"]["inputs"]["motion"] = ["2",0]

    if motion_preset_param:
        if motion_component_param:
            comfy_json["2"]["inputs"]["motion"] = ["1",0]
        else : 
            comfy_json["91"]["inputs"]["motion"] = ["1",0]
        
    if effect:
        comfy_json["91"]["inputs"]["effects"] = ["3",0]
    
    if musique_param:
        comfy_json["207"]["inputs"]["image"]= ["50",0]
        comfy_json["2"]["inputs"]["feature"] = ["209",0]
        comfy_json["5"]["inputs"]["audio"] = ["204",0]


    #Set output node
    comfy_json["5"]["inputs"]["filename_prefix"] = user_name+"/"+str(timestamp)+"/"+"Video"

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    video_link = get_video(ws, comfy_json)

    
    return video_link



if __name__ == "__main__":

    musique ={"musique_link":"audio_cut.MP3","start_time":"10"}

    print(generate_video("35393166.png",7,"test","17181381",musique_param=musique,motion_component_param=[("type","Sine"),("target","Zoom"),("bias","1"),("amplitude","0.3")],motion_preset_param=[("type","Orbital")]))
