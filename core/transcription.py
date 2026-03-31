import ssl
import os
import subprocess

# --- CONFIGURATION SSL (Pour éviter les erreurs de téléchargement du modèle) ---
ssl._create_default_https_context = ssl._create_unverified_context

class Transcriber:
    def __init__(self):
        # On ne charge pas le modèle au démarrage pour éviter les plantages sur Cloud
        self.model = None

    def load_model(self):
        if self.model is None:
            import whisper
            print("⏳ Chargement de l'IA Whisper...")
            self.model = whisper.load_model("base")

    def transcrire(self, video_path):
        # Charge le modèle seulement au moment de la transcription
        self.load_model()
        print(f"👂 L'IA analyse chaque mot : {video_path}")

        # --- CRÉATION D'UN CHEMIN TEMPORAIRE DANS /tmp ---
        base_name = os.path.basename(video_path)
        audio_path = os.path.join("/tmp", base_name.replace(".mp4", "_temp.wav").replace(".mov", "_temp.wav"))

        try:
            # --- EXTRACTION DE L'AUDIO VIA FFMPEG ---
            command = [
                "ffmpeg", "-i", video_path,
                "-vn", "-acodec", "pcm_s16le",
                "-ar", "16000", "-ac", "1",
                audio_path, "-y"
            ]
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # --- TRANSCRIPTION AVEC WHISPER ---
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

            # --- NETTOYAGE ---
            if os.path.exists(audio_path):
                os.remove(audio_path)

            return words_data

        except Exception as e:
            print(f"❌ Erreur lors de la transcription : {e}")
            if os.path.exists(audio_path):
                os.remove(audio_path)
            return []