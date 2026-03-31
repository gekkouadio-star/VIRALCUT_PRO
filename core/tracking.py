import json
from datetime import datetime
import os

class ActivityTracker:
    def __init__(self, log_file="exports/activity_log.json"):
        self.log_file = log_file
        # Créer le dossier exports s'il n'existe pas
        if not os.path.exists("exports"):
            os.makedirs("exports")
        
        # Initialiser le fichier s'il n'existe pas
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f)

    def log_generation(self, url, num_clips, duration):
        """ Enregistre une nouvelle session de création """
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "url": url,
            "clips_count": num_clips,
            "total_processing_time": f"{duration:.2f}s"
        }
        
        with open(self.log_file, 'r+') as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=4)
        
        print(f"📊 Activité enregistrée dans {self.log_file}")