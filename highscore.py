"""
FICHIER OPTIONNEL - PAS INDISPENSABLE

highscore.py
Gestionnaire moderne des meilleurs scores avec sauvegarde JSON.

CE FICHIER N'EST PAS OBLIGATOIRE POUR LANCER LE JEU !
   - Le jeu fonctionne parfaitement sans highscores
   - En cas d'erreur d'import, le système se désactive automatiquement
   - Pour désactiver complètement : mettre ENABLE_HIGHSCORE = False dans settings.py

POUR LANCER LE JEU DE BASE :
   python controller.py
"""
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any


class HighScoreManager:
    """Gestionnaire moderne des scores avec sauvegarde persistante"""
    
    def __init__(self):
        # Dossier de données utilisateur (standard moderne)
        # C:\Users\VOTRE_NOM\.aventurier_game\highscores.json
        # self.data_dir = Path.home() / ".aventurier_game"
        self.data_dir = Path(__file__).parent
        self.score_file = self.data_dir / "highscores.json"
        self.data_dir.mkdir(exist_ok=True)
    
    def load_data(self) -> Dict[str, Any]:
        """Charge les données de score depuis le fichier JSON"""
        try:
            if self.score_file.exists():
                # read_text() utilise automatiquement un context manager (with open)
                return json.loads(self.score_file.read_text(encoding='utf-8'))
            return self._get_default_data()
        except (json.JSONDecodeError, OSError):
            # En cas d'erreur, retourner les données par défaut
            return self._get_default_data()
    
    def _get_default_data(self) -> Dict[str, Any]:
        """Retourne la structure de données par défaut"""
        return {
            "best_score": 0,
            "best_score_date": None,
            "games_played": 0,
            "total_monsters_defeated": 0,
            "total_moves": 0
        }
    
    def save_data(self, data: Dict[str, Any]) -> None:
        """Sauvegarde les données dans le fichier JSON"""
        try:
            # write_text() utilise automatiquement un context manager (with open)
            self.score_file.write_text(
                json.dumps(data, indent=2, ensure_ascii=False), 
                encoding='utf-8'
            )
        except OSError:
            # Si la sauvegarde échoue, continuer silencieusement
            # TODO intéressant : logger l'erreur lorsque logging implémenté
            pass
    
    def get_best_score(self) -> int:
        """Retourne le meilleur score actuel"""
        return self.load_data()["best_score"]
    
    def update_stats(self, score: int, monsters_defeated: int, moves: int) -> tuple[bool, int]:
        """
        Met à jour les statistiques avec une nouvelle partie.
        Retourne (is_new_record, ancien_record).
        """
        data = self.load_data()
        old_best_score = data["best_score"]
        is_new_record = False
        
        # Vérifier si c'est un nouveau record
        if score > data["best_score"]:
            data["best_score"] = score
            data["best_score_date"] = datetime.now().isoformat()
            is_new_record = True
        
        # Mettre à jour les statistiques globales
        data["games_played"] += 1
        data["total_monsters_defeated"] += monsters_defeated
        data["total_moves"] += moves
        
        # Sauvegarder
        self.save_data(data)
        
        return is_new_record, old_best_score
    
    def get_stats_summary(self) -> Dict[str, Any]:
        """Retourne un résumé des statistiques pour affichage"""
        data = self.load_data()
        
        # Calculer les moyennes si on a joué des parties
        games_played = data["games_played"]
        if games_played > 0:
            avg_monsters = data["total_monsters_defeated"] / games_played
            avg_moves = data["total_moves"] / games_played
        else:
            avg_monsters = 0
            avg_moves = 0
        
        return {
            "best_score": data["best_score"],
            "best_score_date": data["best_score_date"],
            "games_played": games_played,
            "avg_monsters_per_game": round(avg_monsters, 1),
            "avg_moves_per_game": round(avg_moves, 1)
        }


if __name__ == "__main__":
    print("ATTENTION: Ce fichier gère la sauvegarde des scores.")
    print("Pour lancer le jeu, exécutez : python controller.py")