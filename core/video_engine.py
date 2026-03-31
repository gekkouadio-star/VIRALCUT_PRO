import os
from moviepy import VideoFileClip

class VideoEngine:
    def __init__(self):
        # On définit où les vidéos seront enregistrées par défaut
        self.output_dir = "exports"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def decouper_et_recadrer(self, video_path, start, end, output_name):
        """
        Découpe un segment et le force au format vertical (9:16)
        """
        print(f"🎬 Traitement de : {video_path}...")
        
        # 1. Charger la vidéo
        clip = VideoFileClip(video_path).subclipped(start, end)
        
        # 2. Calculer le recadrage vertical (9:16)
        # On garde toute la hauteur et on coupe les côtés pour centrer
        w, h = clip.size
        target_ratio = 9/16
        target_w = h * target_ratio
        
        # On centre le rectangle 9:16 au milieu de la vidéo 16:9
        x_center = w / 2
        x1 = x_center - (target_w / 2)
        x2 = x_center + (target_w / 2)
        
        # Appliquer le recadrage
        clip_vertical = clip.cropped(x1=x1, y1=0, x2=x2, y2=h)
        
        # 3. Sauvegarder le résultat dans le dossier 'exports'
        final_path = os.path.join(self.output_dir, output_name)
        clip_vertical.write_videofile(final_path, codec="libx264", audio_codec="aac")
        
        print(f"✅ Vidéo sauvegardée sous : {final_path}")
        return final_path