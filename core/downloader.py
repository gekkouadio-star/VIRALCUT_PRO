import yt_dlp
import os

class VideoDownloader:
    def __init__(self, download_path="inputs"):
        self.download_path = download_path
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

    def telecharger(self, url):
        print(f"🌐 Tentative de récupération de la vidéo : {url}")
        
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': f'{self.download_path}/video_telechargee.%(ext)s',
            'noplaylist': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            video_path = f"{self.download_path}/video_telechargee.mp4"
            print(f"✅ Vidéo prête pour l'analyse : {video_path}")
            return video_path
            
        except Exception as e:
            print(f"❌ Erreur lors du téléchargement : {e}")
            return None