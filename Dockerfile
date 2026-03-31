# 1. Utiliser une version stable de Python
FROM python:3.11-slim

# 2. Installer FFmpeg et les bibliothèques système nécessaires
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# 3. Créer le dossier de travail
WORKDIR /app

# 4. Copier les fichiers du projet
COPY . .

# 5. Installer les bibliothèques Python (ton requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# 6. Exposer le port par défaut de Streamlit
EXPOSE 8501

# 7. Lancer l'application
CMD ["streamlit", "run", "viralcut.py", "--server.port=8501", "--server.address=0.0.0.0"]