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


    return history["outputs"]["53"]["gifs"][0]["filename"] # print history to find the filename


def generate_video(image_link,user_name,time_interval_img,timestamp):

    #load workflow in text
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workflow_json = os.path.join(script_dir, 'workflow_video_test.json')

    with open(workflow_json, "r+", encoding="utf-8") as fichier:
        base_json = fichier.read()

    num_image = len(image_link)
    frame_interval_img = time_interval_img * 12   #12 frame/sec
    total_frame = frame_interval_img * num_image  

    #Fade mask can have only 255 frames
    nb_fade_mask = math.ceil(total_frame/255)

    for i in range(num_image):
        #Add IPAdapter Batch
        base_json += ',"{}":'.format(i)
        base_json += ' {"inputs": {"weight": 1,"weight_type": "ease in-out","start_at": 0,"end_at": 1,"embeds_scaling": "V only","encode_batch_size": 0,"model": ["573",0],"ipadapter": ["573",1],"image": ["'+str(i+20)+'",0],"attn_mask": ["713",0]},"class_type": "IPAdapterBatch","_meta": {"title": "IPAdapter Batch (Adv.)"}}'
        
        #if there is more than 255 frame, merge multiple mask
        for j in range(1,nb_fade_mask):
            #Mask
            base_json += ',"{}":'.format(600+i*10+ j)
            base_json += ' {"inputs": {"points_string": "","invert": false,"frames": 96,"width": 512,"height": 512,"interpolation": "linear"},"class_type": "CreateFadeMaskAdvanced","_meta": {"title": "Create Fade Mask Advanced"}}'
            
            #connect mergeMask node
            if j >=2:
                if j == 2:
                    base_json += ',"{}":'.format(3000+i*100+ j)
                    base_json +=  '{ "inputs": {"merge_strategy": "match A","scale_method": "nearest-exact","crop": "disabled","mask_A": ["'+str(600+i*10+ j -1)+'",0],"mask_B": ["'+str(600+i*10+ j)+'",0] },    "class_type": "VHS_MergeMasks",    "_meta": {      "title": "Merge Mask Batches "    }  }'
                if j > 2:
                    base_json += ',"{}":'.format(3000+i*100+ j)
                    base_json +=  '{ "inputs": {"merge_strategy": "match A","scale_method": "nearest-exact","crop": "disabled","mask_A": ["'+str(3000+i*100+ j -1)+'",0],"mask_B": ["'+str(600+i*10+ j)+'",0] },    "class_type": "VHS_MergeMasks",    "_meta": {      "title": "Merge Mask Batches "    }  }'


        #Load image
        base_json += ',"{}":'.format(i + 20)
        base_json +=' {"inputs": {"image": "","upload": "image"},"class_type": "LoadImage","_meta": {"title":"Load Image"}}'
        
    base_json += "}"
    
    #load update workflow in json
    comfy_json = json.loads(base_json)

    for i, link in enumerate(image_link):
        #Load image
        comfy_json[str(20+i)]['inputs']['image'] = "D:/ComfyUi/ComfyUI_windows_portable/ComfyUI/output/"+user_name+"/"+str(timestamp)+"/"+link
       
        #Create Mask
        comfy_json[str(10+i)]['inputs']['frames'] = total_frame #12 frame/sec
        values = []
        for j in range(num_image):
            position = j * frame_interval_img        
            if j == i : 
                values.append(f"{position}:({1.0})") 
                if j+1 != num_image:
                    values.append(f"{(j+1)*frame_interval_img-8}:({1.0})") 
            else :
                values.append(f"{position}:({0.0})")
            
            if j+1 == i:
               values.append(f"{(j+1)*frame_interval_img-8}:({0.0})") 
            
        image_string = ",".join(values)
        image_string = ",".join(values)
        comfy_json[str(10+i)]['inputs']['points_string'] = image_string

    #connect nodes
        if nb_fade_mask >= 2:
            comfy_json[str(i)]["inputs"]["attn_mask"] = [str(3000+100*i+nb_fade_mask),0]
        else :
            comfy_json[str(i)]["inputs"]["attn_mask"] = [str(600+i*10),0]

        if i == 0:
            comfy_json[str(i)]["inputs"]["model"] =  ["573",0]
        else:
            comfy_json[str(i)]["inputs"]["model"] =  [str(i-1),0]



    comfy_json["80"]["inputs"]["model"] = [str(num_image-1),0]

    comfy_json["134"]["inputs"]["batch_size"] = total_frame
    
    #save video
    comfy_json["53"]["inputs"]["filename_prefix"] = user_name+"/"+str(timestamp)+"/"+"Video"



    #with open('updated_comfy.json', 'w', encoding='utf-8') as outfile:
    #    json.dump(comfy_json, outfile, ensure_ascii=False, indent=4)


    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    video_link = get_video(ws, comfy_json)

    
    return video_link
         

if __name__ == "__main__":

    #generate_video(["ComfyUI_00001_.png","ComfyUI_00002_.png"],"test",2,"1717745319.5879269")
