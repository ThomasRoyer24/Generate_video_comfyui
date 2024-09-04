from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

from moviepy.editor import VideoFileClip

def resize_video_9_16(video_clip,original_video_path):


    # Redimensionner la vidéo à 1080x1920 (format 9:16)
    video_clip_resized = video_clip.resize(newsize=(1920, 1080))

    # Exporter la vidéo redimensionnée
    video_clip_resized.write_videofile("resize_" + original_video_path, codec="libx264")





def make_video(video_path):
    # Charger la vidéo et l'image
    video_clip = VideoFileClip(video_path)
    video_width, video_height = video_clip.size

    if video_width != 1920:
        video_clip = resize_video_9_16(video_clip, video_path)
        video_clip = VideoFileClip("resize_" + video_path)

    image_clip = ImageClip("D:/ComfyUi/ComfyUI_windows_portable/ComfyUI/output/test/1234/Comfyui_00007_.png")


    # Définir la durée de l'image pour qu'elle corresponde à la durée de la vidéo
    image_clip = image_clip.set_duration(video_clip.duration)

    # Positionner la vidéo au centre de l'image sans redimensionner
    video_position = ("center", "center")
    video_clip = video_clip.set_position(video_position)

    # Créer un clip composite avec l'image en arrière-plan et la vidéo en premier plan
    final_clip = CompositeVideoClip([image_clip, video_clip])

    # Exporter la vidéo finale avec les dimensions de l'image
    final_clip.write_videofile("fichier_final2.mp4", codec="libx264")


if __name__ == "__main__":
    make_video("0903.mp4")