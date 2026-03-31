from moviepy import TextClip
# On importe les réglages depuis config.py
from config import FONT_COLOR, FONT_SIZE, STROKE_COLOR, STROKE_WIDTH, VIDEO_HEIGHT

class DesignEngine:
    def __init__(self):
        # On peut garder le chemin spécifique pour Mac
        self.font = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
        
        # Dictionnaire de mots clés pour les couleurs et emojis (Logique métier)
        self.highlights = {
            "AGENT": {"color": "#00FF00", "emoji": "🤖"},
            "ENVIRONNEMENT": {"color": "#FF00FF", "emoji": "🌍"},
            "RÉCOMPENSE": {"color": "yellow", "emoji": "💰"},
            "ERREUR": {"color": "red", "emoji": "❌"},
            "ALGORITHME": {"color": "#00FFFF", "emoji": "⚙️"},
            "IMPORTANT": {"color": "#FF4500", "emoji": "🔥"}
        }
        print("🎨 Moteur de Design Pro activé")

    def generer_sous_titres(self, words, video_width, video_height=VIDEO_HEIGHT):
        clips_texte = []
        
        for w in words:
            # Nettoyage pour la détection des mots-clés
            clean_word = w['word'].upper().strip(".,!?")
            
            # Valeurs par défaut tirées de config.py
            current_color = FONT_COLOR
            display_text = w['word']
            
            # Application des "Pépites" (Highlights)
            if clean_word in self.highlights:
                current_color = self.highlights[clean_word]["color"]
                display_text = f"{self.highlights[clean_word]['emoji']} {w['word']}"

            # Création du clip de texte
            txt_clip = TextClip(
                text=display_text.upper(),
                font=self.font,
                font_size=FONT_SIZE,
                color=current_color,
                stroke_color=STROKE_COLOR,
                stroke_width=STROKE_WIDTH,
                method='label'
            )
            
            # Synchronisation temporelle
            txt_clip = txt_clip.with_start(w['start']).with_end(w['end'])

            # --- TON EFFET DE ZOOM (Gardé car il est excellent !) ---
            # Le mot arrive en petit et "pop" à l'écran
            txt_clip = txt_clip.resized(lambda t: 0.8 + (2.0 * t) if t < 0.1 else 1.0)
            
            # Positionnement (70% de la hauteur pour être sous le visage)
            pos_y = int(video_height * 0.7)
            txt_clip = txt_clip.with_position(('center', pos_y))
            
            clips_texte.append(txt_clip)
            
        return clips_texte