import ssl
import os
import subprocess
import whisper

# --- CONFIGURATION SSL ---
# Évite les erreurs de certificat lors du téléchargement automatique du modèle
ssl._create_default_https_context = ssl._create_unverified_context

class Transcriber:
    def __init__(self):
        # On initialise à None pour ne charger l'IA qu'au premier besoin
        self.model = None

    def load_model(self):
        """Charge le modèle Whisper Tiny (optimisé pour le Cloud Gratuit)"""
        if self.model is None:
            print("⏳ Chargement de l'IA Whisper (Version Tiny - Performance)...")
            # "tiny" consomme ~75Mo de RAM contre ~500Mo pour "base"
            try:
                self.model = whisper.load_model("tiny")
                print("✅ Modèle Whisper Tiny chargé avec succès.")
            except Exception as e:
                print(f"❌ Erreur critique au chargement du modèle : {e}")

    def transcrire(self, video_path):
        """Extrait l'audio et transcrit le texte avec horodatage par mot"""
        
        # 1. S'assurer que le modèle est chargé
        self.load_model()
        
        if not self.model:
            print("❌ Impossible de transcrire : Le modèle n'est pas disponible.")
            return []

        print(f"👂 L'IA analyse chaque mot : {video_path}")

        # --- GESTION DES CHEMINS TEMPORAIRES ---
        # Utilisation de /tmp qui est le seul dossier scriptable sur Render/Streamlit Cloud
        base_name = os.path.basename(video_path)
        audio_path = os.path.join("/tmp", base_name.replace(".mp4", "_temp.wav").replace(".mov", "_temp.wav"))

        try:
            # --- EXTRACTION DE L'AUDIO VIA FFMPEG ---
            # Paramètres optimisés pour Whisper (16kHz, Mono)
            command = [
                "ffmpeg", "-i", video_path,
                "-vn", "-acodec", "pcm_s16le",
                "-ar", "16000", "-ac", "1",
                audio_path, "-y"
            ]
            
            # On lance l'extraction audio
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # --- TRANSCRIPTION AVEC WHISPER ---
            # On force le langage "fr" et word_timestamps pour le montage vidéo précis
            result = self.model.transcribe(
                audio_path, 
                language="fr", 
                word_timestamps=True,
                fp16=False  # Crucial : Désactive le calcul GPU car Render utilise uniquement le CPU
            )

            words_data = []
            for segment in result.get("segments", []):
                if "words" in segment:
                    for word in segment["words"]:
                        words_data.append({
                            "word": word["word"].strip().upper(),
                            "start": word["start"],
                            "end": word["end"]
                        })

            print(f"✅ {len(words_data)} mots détectés avec succès !")

            # --- NETTOYAGE ---
            if os.path.exists(audio_path):
                os.remove(audio_path)

            return words_data

        except Exception as e:
            print(f"❌ Erreur lors de la transcription : {e}")
            if os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                except:
                    pass
            return []