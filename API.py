import os
from flask import Flask, request, jsonify, send_file
from Video_outpainting.API_create_image_outpainting_fom_image import generate_image_outpainting

app = Flask(__name__)

# Dossier où les fichiers seront stockés
UPLOAD_FOLDER = './input'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Vérifie si le dossier existe, sinon le créer
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Fonction pour générer un nom de fichier unique
def generate_unique_filename(filename):
    base, extension = os.path.splitext(filename)
    counter = 1
    while True:
        new_filename = f"image_{counter}{extension}"
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)