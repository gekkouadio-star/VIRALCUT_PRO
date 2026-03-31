import ssl
import whisper
import os
import subprocess

# --- CONFIGURATION SSL (Pour éviter les erreurs de téléchargement du modèle) ---
ssl._create_default_https_context = ssl._create_unverified_context

class Transcriber:
    def __init__(self):
        print("Wait... Chargement de l'IA Whisper...")
        # On utilise le modèle "base" pour un bon compromis vitesse/précision sur le Cloud
        self.model = whisper.load_model("base")

    def transcrire(self, video_path):
        print(f"👂 L'IA analyse chaque mot : {video_path}")
        
        # 1. CRÉATION D'UN CHEMIN POUR L'AUDIO TEMPORAIRE
        # On transforme "video.mp4" en "video_audio.wav"
        audio_path = video_path.replace(".mp4", "_temp.wav").replace(".mov", "_temp.wav")
        
        try:
            # 2. EXTRACTION DE L'AUDIO VIA FFMPEG (Ligne de commande système)
            # Cette commande est beaucoup plus stable sur Linux/Streamlit Cloud
            command = [
                "ffmpeg", "-i", video_path,
                "-vn", "-acodec", "pcm_s16le", 
                "-ar", "16000", "-ac", "1", 
                audio_path, "-y"
            ]
            # On lance l'extraction et on attend qu'elle finisse
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # 3. L'IA ANALYSE LE FICHIER WAV GÉNÉRÉ
            result = self.model.transcribe(audio_path, language="fr", word_timestamps=True)
            
            words_data = []
            for segment in result.get("segments", []):
                if "words" in segment:
                    for word in segment["words"]:
                        words_data.append({
                            "word": word["word"].strip().upper(),
                            "start": word["start"],
                            "end": word["end"]
                        })
            
            print(f"✅ {len(words_data)} mots détectés !")
            
            # 4. NETTOYAGE : Supprimer le fichier audio temporaire après usage
            if os.path.exists(audio_path):
                os.remove(audio_path)
                
            return words_data

        except Exception as e:
            print(f"❌ Erreur lors de la transcription : {e}")
            # En cas d'erreur, on tente quand même de nettoyer
            if os.path.exists(audio_path):
                os.remove(audio_path)
            return []