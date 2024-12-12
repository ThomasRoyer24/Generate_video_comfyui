import os
from flask import Flask, request, jsonify, send_file
from Video_outpainting.API_create_image_outpainting_fom_image import generate_image_outpainting
from Depth_flow.API_depth_animation import generate_video_depth

import json
from datetime import datetime

app = Flask(__name__)

# Dossier où les fichiers seront stockés
UPLOAD_FOLDER = '../input'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Vérifie si le dossier existe, sinon le créer
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Fonction pour générer un nom de fichier unique
def generate_unique_filename(filename):
    base, extension = os.path.splitext(filename)
    counter = 1
    
    # Vérifie le type de fichier et définit le préfixe en conséquence
    if extension.lower() in ['.jpg', '.jpeg', '.png']:
        prefix = "image_"
    elif extension.lower() in ['.wav', '.mp3']:
        prefix = "song_"
    else:
        raise ValueError(f"L'extension '{extension}' n'est pas prise en charge. Seuls les fichiers images et audio sont autorisés.")
    
    # Boucle pour générer un nom de fichier unique
    while True:
        new_filename = f"{prefix}{counter}{extension}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        if not os.path.exists(file_path):
            return new_filename
        counter += 1


@app.route('/outpainting', methods=['POST'])
def outpainting():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # Générer un nom de fichier unique
        unique_filename = generate_unique_filename(file.filename)
        # Chemin complet pour stocker le fichier localement
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        

        output = generate_image_outpainting(unique_filename,"test","123")

        output_path = "../output/" + output 
        

        try:
            return send_file(output_path, as_attachment=True), 200
            
            
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
@app.route('/depth', methods=['POST'])
def depth():
    # Vérifier la présence du fichier image (obligatoire)
    if 'image' not in request.files:
        return jsonify({"error": "Image file is missing"}), 400
    image = request.files['image']

    # Vérifier le fichier image a un nom valide
    if image.filename == '':
        return jsonify({"error": "No selected image file"}), 400

    # Récupérer le fichier de musique si présent or False
    musique = request.files.get('musique') or False

    # Récupérer le paramètre JSON 'data' pour les autres valeurs
    try:
        data = json.loads(request.form.get("data"))  # Charger en tant que JSON
    except (TypeError, json.JSONDecodeError) as e:
        return jsonify({"error": "Invalid or missing 'data' JSON"}), 400

    # Enregistrer l'image
    image_filename = generate_unique_filename(image.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    image.save(image_path)

    # Enregistrer la musique si elle est fournie
    musique_filename = None
    if musique and musique.filename != '':
        musique_filename = generate_unique_filename(musique.filename)
        musique_path = os.path.join(app.config['UPLOAD_FOLDER'], musique_filename)
        musique.save(musique_path)


    user_name = data["user_name"]
    duration = data["duration"]
    musique_param = data.get("musique_param", False)
    motion_component_param = data.get("motion_component_param", False)
    motion_preset_param = data.get("motion_preset_param", False)
    effect_param = data.get("effect_param", False)

    date_str = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).strftime("%d-%m-%Y")

    output = generate_video_depth(image_link = image_path,duration = duration,user_name = user_name,timestamp = date_str,musique_link=musique_path,musique_param=musique_param,motion_component_param=motion_component_param,motion_preset_param=motion_preset_param,effect_param=effect_param,model="depth_anything_v2_vits_fp32.safetensors")

    output_path = "../output/"+ user_name+"/"+date_str+"/" + output 
    

    try:
        return send_file(output_path, as_attachment=True), 200
        
        
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    #linux test
    #curl -X POST http://127.0.0.1:5000/depth \-F "image=@0902.pgn" \-F "musique=@audio_cut.mp3" \-F "data={\"start_time_musique\": \"10\", \"duration\": \"30\", \"user_name\": \"test_user\"}"

    #windows
    #curl -X POST http://127.0.0.1:5000/depth -F "image=@0902.png" -F "musique=@audio_cut.mp3" -F "data={\"user_name\": \"thomas\", \"duration\": \"5\", \"motion_component_param\": [[\"type\", \"Sine\"], [\"target\", \"Zoom\"], [\"bias\", \"1\"], [\"amplitude\", \"0.3\"]], \"motion_preset_param\": [[\"type\", \"Orbital\"]]}"


