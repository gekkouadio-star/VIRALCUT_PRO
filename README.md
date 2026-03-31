# VIRALCUT PRO | AI VIDEO SAAS
> **DÉVELOPPÉ PAR GÉRARD K** > *Transformez vos vidéos longues en pépites virales grâce à l'Intelligence Artificielle.*

---

## PRÉSENTATION
**ViralCut Pro** est un écosystème complet de montage vidéo automatisé conçu pour les créateurs de contenu modernes (TikTok, Reels, Shorts). 

L'application analyse le flux audio, détecte les moments forts via un moteur d'intelligence artificielle, recadre la vidéo au format vertical (9:16) et génère des sous-titres dynamiques parfaitement synchronisés.

---

## FONCTIONNALITÉS CLÉS

### 🛠️ Studio de Création
- **Import intelligent** : Support des URLs (YouTube, TikTok, Instagram) via `yt-dlp`.
- **Upload Local** : Glissez-déposez vos fichiers `.mp4` ou `.mov`.
- **Analyse IA** : Transcription ultra-précise avec le modèle **OpenAI Whisper**.
- **Moteur de Design** : Recadrage automatique au centre et ajout de texte stylisé.

### Bibliothèque (Mes Exports)
- Gestion centralisée de tous les clips générés.
- Prévisualisation directe dans le dashboard.
- Boutons de téléchargement et de suppression rapide.

### Paramètres IA
- Configuration du modèle Whisper (Base, Small, Medium).
- Personnalisation esthétique (couleur du texte, taille de police).
- Options de Face-Tracking et génération d'Emojis (Beta).

---

## STRUCTURE DU PROJET

```text
VIRALCUT-PRO/
├── core/               # Moteurs de logique (Transcription, Design, IA)
├── env_pro/            # Environnement virtuel Python
├── exports/            # Stockage des clips vidéo générés
├── inputs/             # Stockage des vidéos sources téléchargées
├── app.py              # Interface Dashboard Streamlit (Main)
├── config.py           # Configuration centralisée du SaaS
├── requirements.txt    # Liste des dépendances Python
└── .gitignore          # Filtre pour les fichiers lourds et secrets