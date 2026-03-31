############################################################
#                                                          #
#                VIRALCUT PRO DASHBOARD                    #
#                                                          #
############################################################

import streamlit as st
import os
import time
import ssl
from moviepy import VideoFileClip, CompositeVideoClip
from core.transcription import Transcriber
from core.design_engine import DesignEngine
from core.intelligence import IntelligenceEngine
from core.downloader import VideoDownloader
import config 

# --- CONFIGURATION INITIALE ---
ssl._create_default_https_context = ssl._create_unverified_context
for folder in ["exports", "inputs"]:
    if not os.path.exists(folder): os.makedirs(folder)

st.set_page_config(page_title="ViralCut Pro Dashboard", page_icon="✂️", layout="wide")

# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        height: 3em; 
        background-color: #FF4B4B; 
        color: white; 
        font-weight: bold; 
    }
    .stSidebar { 
        background-color: #ffffff; 
        border-right: 1px solid #e0e0e0; 
    }
    /* Style pour l'encadré vert du titre */
    .green-header {
        border: 2px solid #28a745;
        padding: 15px;
        border-radius: 10px;
        color: #28a745;
        display: flex;
        justify-content: center;
        align-items: baseline;
        gap: 20px;
        margin-bottom: 25px;
        background-color: rgba(40, 167, 69, 0.1);
    }
    .green-header h1 {
        margin: 0;
        color: #28a745;
    }
    .developer-name {
        font-size: 1.2em;
        font-weight: bold;
        opacity: 0.8;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CHARGEMENT DES MOTEURS ---
@st.cache_resource
def load_engines():
    return Transcriber(), DesignEngine(), IntelligenceEngine(), VideoDownloader()

transcriber, designer, intel, downloader = load_engines()

# --- NAVIGATION À GAUCHE ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4406/4406114.png", width=80)
    st.title("VIRALCUT PRO")
    
    # MENU DE NAVIGATION EN MAJUSCULE
    page = st.radio("NAVIGATION", ["STUDIO DE CRÉATION", "MES EXPORTS", "PARAMÈTRES IA"])
    
    st.divider()
    
    if page == "STUDIO DE CRÉATION":
        st.subheader("RÉGLAGES DU CLIP")
        num_clips = st.slider("Nombre de clips", 1, 10, config.MAX_CLIPS_PER_VIDEO)
        target_duration = st.slider("Durée (sec)", 5, 60, config.DEFAULT_CLIP_DURATION)
        
        st.subheader("APPARENCE")
        # Correction du bug de couleur (Force Hexa)
        default_color = config.FONT_COLOR if str(config.FONT_COLOR).startswith("#") else "#FFFF00"
        custom_color = st.color_picker("Couleur du texte", default_color)
        font_size = st.number_input("Taille police", 10, 200, config.FONT_SIZE)
    
    st.caption(f"VERSION 1.0 - MODE: {config.WHISPER_MODEL}")

# --- PAGE 1 : STUDIO DE CRÉATION ---
if page == "STUDIO DE CRÉATION":
    # TITRE ENCADRÉ EN VERT AVEC NOM DU DÉVELOPPEUR
    st.markdown('''
        <div class="green-header">
            <h1>🎬 STUDIO DE CRÉATION</h1>
            <span class="developer-name">| DÉVELOPPÉ PAR GÉRARD K</span>
        </div>
    ''', unsafe_allow_html=True)
    
    col_input, col_info = st.columns([2, 1])
    
    with col_input:
        source_type = st.segmented_control("TYPE DE SOURCE", ["Lien Web", "Fichier Local"], default="Lien Web")
        
        if source_type == "Lien Web":
            url_input = st.text_input("🔗 LIEN YOUTUBE, TIKTOK OU INSTAGRAM", placeholder="Collez l'URL ici...")
        else:
            uploaded_file = st.file_uploader("IMPORTEZ VOTRE VIDÉO", type=["mp4", "mov"])
            if uploaded_file:
                video_input_path = os.path.join("inputs", uploaded_file.name)
                with open(video_input_path, "wb") as f: f.write(uploaded_file.getbuffer())

    with col_info:
        st.info("💡 **ASTUCE :** L'IA détecte automatiquement les changements de sujet pour créer des transitions propres.")

    if st.button("LANCER LA PRODUCTION"):
        # LOGIQUE DE VÉRIFICATION
        source_ready = (source_type == "Lien Web" and url_input) or (source_type == "Fichier Local" and uploaded_file)
        
        if not source_ready:
            st.warning("VEUILLEZ SÉLECTIONNER UNE VIDÉO.")
        else:
            start_proc = time.time()
            with st.status("PRODUCTION EN COURS...", expanded=True) as status:
                
                # 1. DOWNLOAD
                if source_type == "Lien Web":
                    video_input_path = downloader.telecharger(url_input)
                
                # 2. TRANSCRIPTION
                st.write("👂 ANALYSE VOCALE...")
                words_data = transcriber.transcrire(video_input_path)
                
                # 3. INTELLIGENCE
                st.write("🧠 DÉTECTION DES PÉPITES VIRALES...")
                suggestions = intel.detecter_meilleurs_moments(words_data)[:num_clips]

                # 4. MONTAGE
                st.write("🎥 RENDU DES CLIPS VERTICAUX...")
                clip_source = VideoFileClip(video_input_path)
                
                grid = st.columns(2)
                for i, moment in enumerate(suggestions):
                    with grid[i % 2]:
                        st.subheader(f"CLIP {i+1}")
                        start_t, end_t = moment['start'], min(moment['start'] + target_duration, clip_source.duration)
                        
                        # PROCESSING (SUBCLIP + RESIZE + CROP)
                        base = clip_source.subclipped(start_t, end_t).resized(height=config.VIDEO_HEIGHT)
                        base = base.cropped(x_center=base.w/2, y_center=base.h/2, width=config.VIDEO_WIDTH, height=config.VIDEO_HEIGHT)
                        
                        # SOUS-TITRES AVEC NOUVELLE COULEUR
                        words_ext = [w.copy() for w in words_data if w['start'] >= start_t and w['end'] <= end_t]
                        for w in words_ext: w['start'] -= start_t; w['end'] -= start_t
                        
                        # Génération des paroles via le moteur de design
                        subs = designer.generer_sous_titres(words_ext, config.VIDEO_WIDTH, config.VIDEO_HEIGHT)
                        
                        final = CompositeVideoClip([base] + subs)
                        out = f"exports/viral_{int(time.time())}_{i+1}.mp4"
                        final.write_videofile(out, fps=config.VIDEO_FPS, codec=config.VIDEO_CODEC, audio_codec="aac")
                        
                        st.video(out)
                        st.download_button(f"TÉLÉCHARGER LE CLIP {i+1}", out, file_name=f"clip_{i+1}.mp4")

                clip_source.close()
                status.update(label=f"✅ PRODUCTION TERMINÉE EN {int(time.time()-start_proc)}S", state="complete")
            st.balloons()

# --- PAGE 2 : MES EXPORTS (BIBLIOTHÈQUE) ---
elif page == "MES EXPORTS":
    st.header("📂 BIBLIOTHÈQUE DE VOS CRÉATIONS")
    files = [f for f in os.listdir("exports") if f.endswith(".mp4")]
    
    if not files:
        st.write("AUCUN CLIP GÉNÉRÉ POUR LE MOMENT.")
    else:
        for f in reversed(files):
            col_vid, col_del = st.columns([4, 1])
            with col_vid:
                st.text(f"FICHIER : {f}")
                st.video(f"exports/{f}")
            with col_del:
                if st.button("🗑️ SUPPRIMER", key=f):
                    os.remove(f"exports/{f}")
                    st.rerun()

# --- PAGE 3 : PARAMÈTRES IA ---
elif page == "PARAMÈTRES IA":
    st.header("CONFIGURATION SYSTÈME")
    st.write("ICI VOUS POUVEZ CONFIGURER LES PARAMÈTRES PROFONDS DE L'APPLICATION.")
    st.toggle("ACTIVER LE RECADRAGE AUTOMATIQUE DES VISAGES (FACE-TRACKING)")
    st.toggle("GÉNÉRER DES EMOJIS AUTOMATIQUEMENT")
    st.selectbox("QUALITÉ D'EXPORT", ["720p (RAPIDE)", "1080p (STANDARD)", "4K (LENT)"])