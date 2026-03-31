# On part d'une base Python stable
FROM python:3.11-slim

# On installe les dépendances système (FFmpeg, etc.)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# On prépare le dossier de travail
WORKDIR /app
COPY . .

# On installe les bibliothèques Python
RUN pip install --no-cache-dir -r requirements.txt

# On expose le port de Streamlit
EXPOSE 8501

# Commande pour lancer l'app
CMD ["streamlit", "run", "viralcut.py", "--server.port=8501", "--server.address=0.0.0.0"]