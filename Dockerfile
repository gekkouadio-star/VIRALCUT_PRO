# 1. Utiliser une version Python stable
FROM python:3.11-slim

# 2. Installer FFmpeg et les libs graphiques (Correction libgl1)
USER root
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# 3. Créer le dossier de travail
WORKDIR /app

# 4. Copier les fichiers
COPY . .

# 5. Installer les bibliothèques Python
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 6. Exposer le port
EXPOSE 8501

# 7. Commande de lancement (Assure-toi que le fichier s'appelle bien viralcut.py)
CMD ["streamlit", "run", "viralcut.py", "--server.port=8501", "--server.address=0.0.0.0"]