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


    return history["outputs"]["5"]["gifs"][0]["filename"] # print history to find the filename


def generate_video(image_link,duration,user_name,timestamp,motion_component=False,motion_component_param=False,motion_preset=False,motion_preset_param=False,effect=False,effect_param=False,model="depth_anything_v2_vits_fp32.safetensors"):

    #load workflow in text
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workflow_json = os.path.join(script_dir, 'depth_motions.json')

    with open(workflow_json, "r+", encoding="utf-8") as fichier:
        base_json = fichier.read()


    # modifier le fichier json pour le workflow    
    if motion_component:
        base_json += Motion_component[motion_component]

    if motion_preset:
        base_json += Motion_preset[motion_preset]

    if effect:
        base_json += Effect[effect]

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


    #Set connection nodes
    if motion_component:
        comfy_json["91"]["inputs"]["motion"] = ["2",0]

    if motion_preset:
        if motion_component:
            comfy_json["2"]["inputs"]["motion"] = ["1",0]
        else : 
            comfy_json["91"]["inputs"]["motion"] = ["1",0]
        
    if effect:
        comfy_json["91"]["inputs"]["effects"] = ["3",0]


    #Set output node
    comfy_json["5"]["inputs"]["filename_prefix"] = user_name+"/"+str(timestamp)+"/"+"Video"


        # Sauvegarder le JSON modifié
    output_json_path = os.path.join(script_dir, f'modified_workflow_{timestamp}.json')
    with open(output_json_path, "w", encoding="utf-8") as fichier:
        json.dump(base_json, fichier, indent=4)

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    video_link = get_video(ws, comfy_json)

    
    return video_link

Motion_component = {
    "Sine": ''',"2": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "amplitude",
            "feature_mode": "relative",
            "target": "Isometric",
            "amplitude": 1,
            "cycles": 1,
            "phase": 0,
            "reverse": false,
            "bias": 0,
            "cumulative": false
        },
        "class_type": "DepthflowMotionSine",
        "_meta": {
            "title": "🌊 Depthflow Motion Sine"
        }
    }''',

    "Cosine": ''',"2": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "amplitude",
            "feature_mode": "relative",
            "target": "Isometric",
            "amplitude": 1,
            "cycles": 1,
            "phase": 0,
            "reverse": false,
            "bias": 0,
            "cumulative": false
        },
        "class_type": "DepthflowMotionCosine",
        "_meta": {
            "title": "🌊 Depthflow Motion Cosine"
        }
    }''',

    "Linear": ''',"2": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "start",
            "feature_mode": "relative",
            "target": "Isometric",
            "start": 0,
            "end": 1,
            "low": 0,
            "high": 1,
            "exponent": 1,
            "reverse": false,
            "cumulative": false
        },
        "class_type": "DepthflowMotionLinear",
        "_meta": {
            "title": "🌊 Depthflow Motion Linear"
        }
    }''',

    "Exponential": ''',"2": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "base",
            "feature_mode": "relative",
            "target": "Isometric",
            "base": 2,
            "scale": 1,
            "reverse": false,
            "cumulative": false
        },
        "class_type": "DepthflowMotionExponential",
        "_meta": {
            "title": "🌊 Depthflow Motion Exponential"
        }
    }''',

    "Arc": ''',"2": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "start",
            "feature_mode": "relative",
            "target": "OffsetX",
            "start": -0.5,
            "middle": -0.25,
            "end": 1,
            "reverse": false,
            "cumulative": false
        },
        "class_type": "DepthflowMotionArc",
        "_meta": {
            "title": "🌊 Depthflow Motion Arc"
        }
    }''',

    "Target": ''',"2": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "value",
            "feature_mode": "relative",
            "target": "Height",
            "value": 0.2
        },
        "class_type": "DepthflowMotionSetTarget",
        "_meta": {
            "title": "🌊 Depthflow Motion Set Target"
        }
    }'''
}

# Dictionnaire de données
Motion_preset = {
    "Circle": ''',"1": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "intensity",
            "feature_mode": "relative",
            "intensity": 0.65,
            "reverse": false,
            "smooth": true,
            "phase_x": 0,
            "phase_y": 0,
            "phase_z": 0,
            "amplitude_x": 1,
            "amplitude_y": 1,
            "amplitude_z": 0,
            "static_value": 0.3
        },
        "class_type": "DepthflowMotionPresetCircle",
        "_meta": {
            "title": "🌊 Depthflow Motion Preset Circle"
        }
    }''',

    "Dolly": ''',"1": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "intensity",
            "feature_mode": "relative",
            "intensity": 0.8,
            "reverse": false,
            "smooth": true,
            "loop": true,
            "depth": 0.5
        },
        "class_type": "DepthflowMotionPresetDolly",
        "_meta": {
            "title": "🌊 Depthflow Motion Preset Dolly"
        }
    }''',

    "Horizontal": ''',"1": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "intensity",
            "feature_mode": "relative",
            "intensity": 0.8,
            "reverse": false,
            "loop": true,
            "smooth": true,
            "phase": 0,
            "steady_value": 0.3
        },
        "class_type": "DepthflowMotionPresetHorizontal",
        "_meta": {
            "title": "🌊 Depthflow Motion Preset Horizontal"
        }
    }''',

    "Vertical": ''',"1": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "intensity",
            "feature_mode": "relative",
            "intensity": 0.8,
            "reverse": false,
            "loop": true,
            "smooth": true,
            "phase": 0,
            "steady_value": 0.3
        },
        "class_type": "DepthflowMotionPresetVertical",
        "_meta": {
            "title": "🌊 Depthflow Motion Preset Vertical"
        }
    }''',

    "Zoom": ''',"1": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "intensity",
            "feature_mode": "relative",
            "intensity": 0.8,
            "reverse": false,
            "smooth": true,
            "phase": 0,
            "loop": false
        },
        "class_type": "DepthflowMotionPresetZoom",
        "_meta": {
            "title": "🌊 Depthflow Motion Preset Zoom"
        }
    }''',

    "Orbital": ''',"1": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "intensity",
            "feature_mode": "relative",
            "intensity": 0.8,
            "reverse": false,
            "depth": 0.5
        },
        "class_type": "DepthflowMotionPresetOrbital",
        "_meta": {
            "title": "🌊 Depthflow Motion Preset Orbital"
        }
    }'''
}

Effect = {
    "DOF": ''',"3": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "dof_intensity",
            "feature_mode": "absolute",
            "dof_enable": true,
            "dof_start": 0.3,
            "dof_end": 1,
            "dof_exponent": 2,
            "dof_intensity": 1,
            "dof_quality": 16,
            "dof_directions": 16
        },
        "class_type": "DepthflowEffectDOF",
        "_meta": {
            "title": "🌊 Depthflow Effect DOF"
        }
    }''',

    "Vignette": ''',"3": {
        "inputs": {
            "strength": 1,
            "feature_threshold": 0,
            "feature_param": "vignette_intensity",
            "feature_mode": "relative",
            "vignette_enable": true,
            "vignette_intensity": 30,
            "vignette_decay": 0.8
        },
        "class_type": "DepthflowEffectVignette",
        "_meta": {
            "title": "🌊 Depthflow Effect Vignette"
        }
    }'''
}


if __name__ == "__main__":

    print(generate_video("ComfyUI_00046_.png",8,"test","17181381",motion_component="Sine",motion_component_param=[("target","Zoom"),("bias","1"),("amplitude","0.3")],motion_preset = "Orbital"))
