import os

# --- CHEMINS DES DOSSIERS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "inputs")
EXPORT_DIR = os.path.join(BASE_DIR, "exports")

# --- PARAMÈTRES VIDÉO (Vertical TikTok/Reels) ---
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 24
VIDEO_CODEC = "libx264"

# --- DESIGN DES SOUS-TITRES (Paroles) ---
FONT_NAME = "Arial-Bold" # Assure-toi que la police est installée sur ton Mac
FONT_SIZE = 70
FONT_COLOR = "#FFFF00"
STROKE_COLOR = "black"
STROKE_WIDTH = 2

# --- INTELLIGENCE & WHISPER ---
WHISPER_MODEL = "base"  # Options: tiny, base, small, medium, large
DEFAULT_CLIP_DURATION = 15 # secondes
MAX_CLIPS_PER_VIDEO = 5

# --- MOTS CLÉS POUR LE DÉCOUPAGE ---
KEYWORDS = [
    "IMPORTANT", "DÉFINITION", "AGENT", "RÉCOMPENSE", 
    "ALGORITHME", "CONCRET", "EXEMPLE", "MÉTHODE"
]