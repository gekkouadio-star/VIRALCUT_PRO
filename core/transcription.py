import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import whisper

class Transcriber:
    def __init__(self):
        print("Wait... Chargement de l'IA Whisper...")
        self.model = whisper.load_model("base")

    def transcrire(self, video_path):
        print(f"👂 L'IA analyse chaque mot : {video_path}")
        # On utilise bien video_path ici (l'argument de la fonction)
        result = self.model.transcribe(video_path, language="fr", word_timestamps=True)
        
        words_data = []
        for segment in result["segments"]:
            # Whisper ajoute une liste 'words' dans chaque segment grâce à word_timestamps=True
            if "words" in segment:
                for word in segment["words"]:
                    words_data.append({
                        "word": word["word"].strip().upper(),
                        "start": word["start"],
                        "end": word["end"]
                    })
        
        print(f"✅ {len(words_data)} mots détectés !")
        return words_data