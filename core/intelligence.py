import json

class IntelligenceEngine:
    def __init__(self):
        # Liste des mots-clés "piliers" pour détecter un moment important dans un cours
        self.mots_cles = [
            "IMPORTANT", "DÉFINITION", "AGENT", "RÉCOMPENSE", 
            "ENVIRONNEMENT", "ALGORITHME", "EXEMPLE", "CONCRET",
            "TRANSFORMATION", "ERREUR", "APPRENTISSAGE", "MÉTHODE"
        ]
        print("⚙️ Moteur d'analyse logique activé (Zéro frais API)")

    def detecter_meilleurs_moments(self, words_data):
        """
        Analyse la liste des mots issus de Whisper pour trouver 3 séquences clés.
        """
        print("🔍 Scan de la transcription pour trouver les passages clés...")
        
        suggestions = []
        # On récupère la fin de la vidéo
        duree_max = words_data[-1]['end']
        
        # On scanne la vidéo par tranches de 30 secondes pour varier les sujets
        pas_de_scan = 30 
        
        for start_v in range(0, int(duree_max), pas_de_scan):
            end_v = start_v + 15 # On crée des clips de 15 secondes
            
            # On extrait tous les mots présents dans cette fenêtre de 15s
            mots_fenetre = [w['word'].upper() for w in words_data if start_v <= w['start'] <= end_v]
            texte_fenetre = " ".join(mots_fenetre)
            
            # On vérifie si un de nos mots-clés est présent dans ce texte
            for mot in self.mots_cles:
                if mot in texte_fenetre:
                    # On a trouvé un intérêt ! On enregistre ce moment.
                    suggestions.append({
                        "start": start_v,
                        "end": end_v,
                        "reason": f"Focus_{mot.capitalize()}"
                    })
                    break # On arrête de chercher d'autres mots pour cette fenêtre
            
            # On s'arrête dès qu'on a 3 clips pour ce premier test automatique
            if len(suggestions) >= 3:
                break

        # Sécurité : si aucun mot n'est trouvé parmi les 7000 mots (peu probable)
        if not suggestions:
            print("⚠️ Aucun mot-clé détecté, utilisation du moment par défaut (783s).")
            return [{"start": 783, "end": 798, "reason": "Extrait_Manuel"}]
            
        print(f"✅ {len(suggestions)} passages détectés avec succès.")
        return suggestions