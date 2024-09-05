from PIL import Image
import os

def reshape_image2(image_path) :
    
    # Charger l'image d'origine
    image = Image.open(image_path)

    # Taille d'origine
    original_width, original_height = image.size

    # Calculer les dimensions des marges
    margin_width = original_width // 5
    margin_height = original_height // 6

    # Calculer les nouvelles dimensions cibles
    target_width = original_width + 2 * margin_width
    target_height = original_height + 2 * margin_height

    # Créer une nouvelle image avec un fond blanc
    new_image = Image.new("RGB", (target_width, target_height), (255, 255, 255))

    # Coller l'image d'origine au centre de la nouvelle image
    new_image.paste(image, (margin_width, margin_height))

    # Obtenir le nom de fichier et l'extension
    base, ext = os.path.splitext(image_path)

    # Créer le nouveau nom de fichier
    new_image_path = f"{base}_reshape{ext}"

    # Sauvegarder l'image
    new_image.save(new_image_path)

    

def reshape_image(image_path,user_name,timestamp) :
    path_original_image = "D:/ComfyUi/ComfyUI_windows_portable/ComfyUI/output/"+user_name+"/"+str(timestamp)+"/"+image_path

    # Charger l'image d'origine
    image = Image.open(path_original_image)

    # Taille d'origine
    original_width, original_height = image.size

    # Calculer les dimensions des marges
    margin_width = original_width // 3
    margin_height = original_height // 4

    # Calculer les nouvelles dimensions cibles
    target_width = original_width + 2 * margin_width
    target_height = original_height + 2 * margin_height

    # Créer une nouvelle image avec un fond blanc
    new_image = Image.new("RGB", (target_width, target_height), (255, 255, 255))

    # Coller l'image d'origine au centre de la nouvelle image
    new_image.paste(image, (margin_width, margin_height))

    # Obtenir le nom de fichier et l'extension
    base, ext = os.path.splitext(image_path)

    # Créer le nouveau nom de fichier
    new_image_path = f"{base}_reshape{ext}"


    path_new_image = "D:/ComfyUi/ComfyUI_windows_portable/ComfyUI/output/"+user_name+"/"+str(timestamp)+"/"+new_image_path
    # Sauvegarder l'image
    new_image.save(path_new_image)

    return new_image_path


if __name__ == "__main__":
    reshape_image2("1 (10).png")