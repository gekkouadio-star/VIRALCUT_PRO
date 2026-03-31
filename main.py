import os
import ssl
import sys

# Correction pour le téléchargement des modèles IA sur Mac
ssl._create_default_https_context = ssl._create_unverified_context

from moviepy import VideoFileClip, CompositeVideoClip
from core.transcription import Transcriber
from core.design_engine import DesignEngine
from core.intelligence import IntelligenceEngine
from core.downloader import VideoDownloader # Importation du nouveau module

# 1. Initialisation des moteurs
print("\n🎬 --- INITIALISATION DE VIRALCUT PRO (MASTER) ---")
downloader = VideoDownloader()
transcriber = Transcriber()
designer = DesignEngine()
intel = IntelligenceEngine()

# --- NOUVEAU : Sélection de la source ---
print("\n🔗 Entrez une URL (YouTube, TikTok, Reels) ou appuyez sur Entrée pour utiliser 'inputs/test.mp4'")
url_input = input("URL ou Chemin : ").strip()

if url_input.startswith("http"):
    # On télécharge la vidéo via le lien
    video_input = downloader.telecharger(url_input)
    if not video_input:
        print("❌ Échec du téléchargement. Arrêt du programme.")
        sys.exit()
elif url_input == "":
    video_input = "inputs/test.mp4"
else:
    video_input = url_input

# Vérification finale de l'existence du fichier
if not os.path.exists(video_input):
    print(f"❌ Fichier {video_input} introuvable !")
    sys.exit()

# 2. Transcription intégrale (Analyse sonore)
print(f"\n👂 Étape 1 : Analyse sonore complète avec Whisper ({video_input})...")
words_data = transcriber.transcrire(video_input)
print(f"✅ {len(words_data)} mots détectés.")

# 3. Intelligence Artificielle : Choix des meilleurs moments
print("\n🧠 Étape 2 : L'IA sélectionne les moments les plus viraux...")
suggestions = intel.detecter_meilleurs_moments(words_data)

# 4. Boucle de création de clips (Production en série)
print(f"\n🎥 {len(suggestions)} clips vont être générés. Lancement de la production...")

# Chargement de la source une seule fois
clip_source = VideoFileClip(video_input)

for index, moment in enumerate(suggestions):
    start_t = moment['start']
    end_t = moment['end']
    # Nettoyage du nom pour éviter les erreurs de fichier
    nom_clip = moment['reason'].replace(" ", "_").replace("'", "").lower()
    
    print(f"\n🎬 --- Création du Clip {index + 1}/{len(suggestions)} : {moment['reason']} ---")
    
    try:
        # Découpage du passage
        base_clip = clip_source.subclipped(start_t, end_t)

        # Recadrage vertical (TikTok/Reels 1080x1920)
        # 1. On redimensionne pour que la hauteur soit 1920
        base_clip = base_clip.resized(height=1920)
        
        # 2. On centre et on coupe les bords pour avoir 1080 de large
        x_center = int(base_clip.w / 2)
        y_center = int(base_clip.h / 2)
        base_clip = base_clip.cropped(x_center=x_center, y_center=y_center, width=1080, height=1920)

        # Filtrage et recalage des mots pour ce clip précis
        words_extraits = [w.copy() for w in words_data if w['start'] >= start_t and w['end'] <= end_t]
        for w in words_extraits:
            w['start'] -= start_t
            w['end'] -= start_t

        # Génération des sous-titres dynamiques (Design Engine)
        subtitle_clips = designer.generer_sous_titres(words_extraits, 1080, 1920)

        # Fusion finale des couches (Vidéo + Texte)
        final_video = CompositeVideoClip([base_clip] + subtitle_clips)

        # Exportation
        if not os.path.exists("exports"):
            os.makedirs("exports")
            
        output_path = f"exports/viral_{index + 1}_{nom_clip}.mp4"
        final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", temp_audiofile="temp-audio.m4a", remove_temp=True)
        
        print(f"✅ Terminé : {output_path}")

    except Exception as e:
        print(f"❌ Erreur lors de la création du clip {index + 1} : {e}")

# Nettoyage
clip_source.close()
print("\n🚀 TOUS LES CLIPS SONT PRÊTS ! Regarde dans le dossier 'exports/'.")