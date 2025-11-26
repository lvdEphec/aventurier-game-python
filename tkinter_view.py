"""
# Il serait préférable de placer tous les messages affichés dans un dictionnaire dans un fichier textes.py.
# Exemple : TEXTES = {"game_over": "GAME OVER !", ...}
🎮 FICHIER OPTIONNEL - PAS INDISPENSABLE 🎮

tkinter_view.py
Interface graphique avec tkinter pour le jeu Aventurier.

⚠️ CE FICHIER N'EST PAS OBLIGATOIRE POUR LANCER LE JEU !
   - Le jeu fonctionne parfaitement en mode console uniquement
   - En cas d'erreur tkinter, choisir l'option "1. Mode Console"
   - Compatible avec le controller existant grâce aux mêmes méthodes

✅ POUR LANCER LE JEU DE BASE :
   python controller.py  →  choix "1"

💡 Avantage de tkinter : Inclus par défaut avec Python (pas d'installation nécessaire).

⚠️ Ce fichier a été généré par Intelligence Artificielle (GitHub Copilot)
   et peut nécessiter des ajustements selon vos besoins spécifiques.
"""
import tkinter as tk
from tkinter import messagebox, ttk
import queue
from settings import PlayerAction, GRID_SIZE


class TkinterView:
    """Interface graphique complète pour le jeu Aventurier"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎮 AVENTURIER - Jeu d'Aventure")
        self.root.geometry("1200x600")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(True, True)  # Permettre le redimensionnement
        
        # Queue pour la communication thread-safe avec le controller
        self.action_queue = queue.Queue()
        self.waiting_for_input = False
        
        # Variables d'affichage
        self.board_buttons = []
        self.message_var = tk.StringVar(value="Bienvenue dans l'aventure !")
        
        self._create_interface()
        self._setup_key_bindings()
        
        # Centrer la fenêtre
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"1200x600+{x}+{y}")
    
    def _create_interface(self):
        """Créé l'interface complète"""
        
        # === TITRE AVEC STATS (SIMPLIFIÉ) ===
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(fill=tk.X, pady=10)
        
        # Titre à gauche
        title_label = tk.Label(
            title_frame,
            text="🗡️ AVENTURIER 🗡️",
            font=('Arial', 24, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        title_label.pack(side=tk.LEFT)
        
        # Bouton Quitter à droite
        self.btn_quit = tk.Button(
            title_frame,
            text="❌ Quitter",
            font=('Arial', 12, 'bold'),
            bg='#e67e22',
            fg='white',
            command=lambda: self._send_action(PlayerAction.QUIT),
            relief=tk.RAISED,
            bd=2
        )
        self.btn_quit.pack(side=tk.RIGHT, padx=(0, 20))  # Un peu moins à droite
        
        # Stats au centre
        stats_center = tk.Frame(title_frame, bg='#2c3e50')
        stats_center.pack(side=tk.LEFT, padx=(50, 0))
        
        hp_label = tk.Label(
            stats_center,
            text="❤️ HP:",
            font=('Arial', 16, 'bold'),
            fg='#e74c3c',
            bg='#2c3e50'
        )
        hp_label.pack(side=tk.LEFT)
        
        self.hp_title = tk.Label(
            stats_center,
            text="5",
            font=('Courier', 16, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        self.hp_title.pack(side=tk.LEFT, padx=(5, 20))
        
        force_label = tk.Label(
            stats_center,
            text="⚔️ Force:",
            font=('Arial', 16, 'bold'),
            fg='#3498db',
            bg='#2c3e50'
        )
        force_label.pack(side=tk.LEFT)
        
        self.force_title = tk.Label(
            stats_center,
            text="10",
            font=('Courier', 16, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        self.force_title.pack(side=tk.LEFT, padx=(5, 0))
        
        # === FRAME PRINCIPAL ===
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # === PLATEAU DE JEU (GAUCHE) ===
        board_frame = tk.LabelFrame(
            main_frame,
            text="🗺️ Plateau de Jeu",
            font=('Arial', 14, 'bold'),
            fg='#ecf0f1',
            bg='#34495e',
            relief=tk.RAISED,
            bd=3
        )
        board_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Grille du plateau
        self.board_grid = tk.Frame(board_frame, bg='#34495e')
        self.board_grid.pack(expand=True, pady=20)
        
        # Initialiser la grille de boutons
        self.board_buttons = []
        for row in range(GRID_SIZE):
            button_row = []
            for col in range(GRID_SIZE):
                btn = tk.Button(
                    self.board_grid,
                    text="·",
                    font=('Courier', 16, 'bold'),
                    width=4,
                    height=2,
                    bg='#95a5a6',
                    fg='#2c3e50',
                    relief=tk.RAISED,
                    bd=2,
                    state=tk.DISABLED
                )
                btn.grid(row=row, column=col, padx=2, pady=2)
                button_row.append(btn)
            self.board_buttons.append(button_row)
        
        # === PANNEAU DE CONTRÔLE (DROITE) ===
        control_frame = tk.LabelFrame(
            main_frame,
            text="🎮 Contrôles & Infos",
            font=('Arial', 14, 'bold'),
            fg='#ecf0f1',
            bg='#34495e',
            relief=tk.RAISED,
            bd=3
        )
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        control_frame.configure(width=600)  # MAXIMUM de largeur !
        control_frame.pack_propagate(False)
        
        # --- Contrôles de déplacement ---
        controls_frame = tk.LabelFrame(
            control_frame,
            text="🕹️ Déplacements",
            font=('Arial', 12, 'bold'),  # Plus gros
            fg='#ecf0f1',
            bg='#34495e'
        )
        controls_frame.pack(fill=tk.X, padx=10, pady=8)  # Plus d'espace
        
        # Grille de boutons directionnels
        btn_grid = tk.Frame(controls_frame, bg='#34495e')
        btn_grid.pack(pady=5)  # Moins d'espace vertical
        
        # Boutons avec taille plus confortable mais moins hauts
        btn_style = {
            'font': ('Arial', 12, 'bold'),
            'width': 4,
            'height': 1,  # Moins haut !
            'relief': tk.RAISED,
            'bd': 2
        }
        
        # Haut
        self.btn_up = tk.Button(
            btn_grid,
            text="↑",
            bg='#3498db',
            fg='white',
            command=lambda: self._send_action(PlayerAction.MOVE_UP),
            **btn_style
        )
        self.btn_up.grid(row=0, column=1, padx=2, pady=2)
        
        # Gauche, Attaque, Droite
        self.btn_left = tk.Button(
            btn_grid,
            text="←",
            bg='#3498db',
            fg='white',
            command=lambda: self._send_action(PlayerAction.MOVE_LEFT),
            **btn_style
        )
        self.btn_left.grid(row=1, column=0, padx=2, pady=2)
        
        self.btn_attack = tk.Button(
            btn_grid,
            text="⚔️",
            bg='#e74c3c',
            fg='white',
            command=lambda: self._send_action(PlayerAction.ATTACK),
            **btn_style
        )
        self.btn_attack.grid(row=1, column=1, padx=2, pady=2)
        
        self.btn_right = tk.Button(
            btn_grid,
            text="→",
            bg='#3498db',
            fg='white',
            command=lambda: self._send_action(PlayerAction.MOVE_RIGHT),
            **btn_style
        )
        self.btn_right.grid(row=1, column=2, padx=2, pady=2)
        
        # Bas
        self.btn_down = tk.Button(
            btn_grid,
            text="↓",
            bg='#3498db',
            fg='white',
            command=lambda: self._send_action(PlayerAction.MOVE_DOWN),
            **btn_style
        )
        self.btn_down.grid(row=2, column=1, padx=2, pady=2)
        
        # --- Messages (MAXIMISÉS) ---
        message_frame = tk.LabelFrame(
            control_frame,
            text="💬 JOURNAL DE L'AVENTURE",
            font=('Arial', 12, 'bold'),
            fg='#f39c12',
            bg='#34495e'
        )
        message_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)  # Plus d'espace
        
        # Frame pour le texte et scrollbar
        text_frame = tk.Frame(message_frame, bg='#34495e')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.message_text = tk.Text(
            text_frame,
            font=('Consolas', 13, 'normal'),  # Police plus grosse
            bg='#1a1a1a',
            fg='#ecf0f1',
            wrap=tk.WORD,
            height=20,  # ENCORE plus haut !
            state=tk.DISABLED,
            relief=tk.RAISED,
            bd=3,
            padx=15,
            pady=12,
            selectbackground='#3498db',
            insertbackground='#ecf0f1'
        )
        self.message_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar pour les messages
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.message_text.yview)
        
        # Configurer les tags de couleurs pour les messages
        self._configure_message_tags()
        
        # Gestion de fermeture
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _configure_message_tags(self):
        """Configure les tags de couleurs pour les messages"""
        # Style pour différents types de messages avec polices plus grosses
        self.message_text.tag_configure('info', foreground='#3498db', font=('Consolas', 12, 'normal'))
        self.message_text.tag_configure('success', foreground='#27ae60', font=('Consolas', 12, 'bold'))
        self.message_text.tag_configure('warning', foreground='#f39c12', font=('Consolas', 12, 'bold'))
        self.message_text.tag_configure('error', foreground='#e74c3c', font=('Consolas', 12, 'bold'))
        self.message_text.tag_configure('combat', foreground='#e67e22', font=('Consolas', 12, 'bold'))
        self.message_text.tag_configure('action', foreground='#9b59b6', font=('Consolas', 12, 'normal'))
        self.message_text.tag_configure('victory', foreground='#2ecc71', font=('Consolas', 13, 'bold'))
        self.message_text.tag_configure('title', foreground='#f1c40f', font=('Consolas', 13, 'bold'))
        
        # Message d'accueil avec style
        self.message_text.config(state=tk.NORMAL)
        self.message_text.insert(tk.END, "═══════════════════════════════════════\n", 'title')
        self.message_text.insert(tk.END, "🗡️  BIENVENUE DANS L'AVENTURE !  🗡️\n", 'title')
        self.message_text.insert(tk.END, "═══════════════════════════════════════\n\n", 'title')
        self.message_text.insert(tk.END, "🎯 Atteignez l'arrivée (🏁) en évitant les monstres !\n", 'info')
        self.message_text.insert(tk.END, "⚔️  Combattez ou fuyez selon votre stratégie !\n\n", 'info')
        self.message_text.config(state=tk.DISABLED)
    
    def _setup_key_bindings(self):
        """Configure les raccourcis clavier"""
        self.root.bind('<Key>', self._on_key_press)
        self.root.focus_set()  # Pour recevoir les événements clavier
    
    def _on_key_press(self, event):
        """Gère les touches du clavier"""
        key_actions = {
            'Up': PlayerAction.MOVE_UP,
            'Down': PlayerAction.MOVE_DOWN,
            'Left': PlayerAction.MOVE_LEFT,
            'Right': PlayerAction.MOVE_RIGHT,
            'space': PlayerAction.ATTACK,
            'Escape': PlayerAction.QUIT
        }
        
        if event.keysym in key_actions:
            self._send_action(key_actions[event.keysym])
    
    def _send_action(self, action):
        """Envoie une action au controller"""
        if self.waiting_for_input:
            self.action_queue.put(action)
            self.waiting_for_input = False
    
    def _on_closing(self):
        """Gestion de fermeture de fenêtre"""
        self._send_action(PlayerAction.QUIT)
    
    def _add_message(self, message, msg_type='info'):
        """Ajoute un message coloré à la zone de texte"""
        self.message_text.config(state=tk.NORMAL)
        
        # Ajouter horodatage pour certains messages importants
        import datetime
        if msg_type in ['combat', 'success', 'error', 'victory']:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            self.message_text.insert(tk.END, f"[{timestamp}] ", 'info')
        
        self.message_text.insert(tk.END, f"{message}\n", msg_type)
        self.message_text.see(tk.END)
        self.message_text.config(state=tk.DISABLED)
        
        # Forcer la mise à jour de l'affichage
        self.root.update()
        self.root.update_idletasks()
    
    def clear_screen(self):
        """Méthode pour compatibilité avec ConsoleView (ne fait rien en GUI)"""
        pass  # En GUI, pas besoin de clearer l'écran

    def display_board(self, hero, board):
        """Affiche le plateau de jeu mis à jour"""
        # Réinitialiser tous les boutons
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                btn = self.board_buttons[row][col]
                btn.config(text="·", bg='#95a5a6', fg='#2c3e50')
        
        # Position de départ et d'arrivée
        self.board_buttons[0][0].config(text="🚪", bg='#27ae60', fg='white')  # Départ
        self.board_buttons[GRID_SIZE-1][GRID_SIZE-1].config(text="🏁", bg='#27ae60', fg='white')  # Arrivée
        
        # Placer les monstres
        for monster in board.monsters:
            if 0 <= monster.x < GRID_SIZE and 0 <= monster.y < GRID_SIZE:
                self.board_buttons[monster.y][monster.x].config(
                    text="👹", bg='#e74c3c', fg='white'
                )
        
        # Placer les équipements
            for equipment in board.equipments:
                if equipment.position is not None:
                    if 0 <= equipment.x < GRID_SIZE and 0 <= equipment.y < GRID_SIZE:
                        # Vérifier qu'il n'y a pas de monstre à cette position
                        # Generator expression avec any() : s'arrête dès qu'un monstre est trouvé
                        monster_here = any(m.x == equipment.x and m.y == equipment.y for m in board.monsters)
                        if not monster_here:
                            self.board_buttons[equipment.y][equipment.x].config(
                                text="📦", bg='#f39c12', fg='white'
                            )
        
        # Placer le héros (en dernier pour qu'il soit visible)
        if 0 <= hero.x < GRID_SIZE and 0 <= hero.y < GRID_SIZE:
            self.board_buttons[hero.y][hero.x].config(
                text="🦸", bg='#3498db', fg='white'
            )
        
        self.root.update_idletasks()
    
    def show_stats(self, hero):
        """Met à jour les statistiques affichées (dans le titre)"""
        self.hp_title.config(text=f"{hero.hp}")
        self.force_title.config(text=f"{hero.force}")
    
    def show_action_message(self, message):
        """Affiche un message d'action avec la couleur appropriée"""
        # Déterminer le type de message selon son contenu
        if "vaincu" in message.lower() or "🎉" in message:
            self._add_message(f"🎯 {message}", 'success')
        elif "coup réussi" in message.lower() or "💥" in message:
            self._add_message(f"🎯 {message}", 'combat')
        elif "coup raté" in message.lower() or "💔" in message:
            self._add_message(f"🎯 {message}", 'warning')
        else:
            self._add_message(f"🎯 {message}", 'action')
    
    def show_combat_prompt(self):
        """Affiche le prompt de combat"""
        self._add_message("\n⚔️ COMBAT ! Attaquez (ESPACE/⚔️) ou déplacez-vous pour fuir !\n", 'combat')
    
    def get_player_input(self):
        """Récupère l'input du joueur de manière non-bloquante"""
        self.waiting_for_input = True
        
        # Boucle d'attente pour l'input
        while self.waiting_for_input:
            self.root.update()
            try:
                action = self.action_queue.get_nowait()
                return action
            except queue.Empty:
                continue
        
        # Si on arrive ici, il y a une action en attente
        try:
            return self.action_queue.get_nowait()
        except queue.Empty:
            return PlayerAction.UNKNOWN
    
    def format_combat_message(self, combat_result, hero_score):
        """Formate un message de combat (retourne juste le texte, sans l'afficher)"""
        if combat_result.monster_died:
            return f"🎉 Monstre vaincu ! Score: {hero_score}"
        elif combat_result.hit:
            return f"💥 Coup réussi ! Monstre: {combat_result.monster_hp}/{combat_result.monster_max_hp} HP"
        else:
            return f"💔 Coup raté ! Héros: {combat_result.hero_hp}/{combat_result.hero_max_hp} HP"
    
    def show_game_over(self, hero):
        """Affiche l'écran de game over"""
        self._add_message("\n══════════════════════════════════════════", 'error')
        self._add_message("💀 GAME OVER ! Vous êtes mort...", 'error')
        self._add_message("══════════════════════════════════════════\n", 'error')
        
        # Afficher les statistiques finales dans la zone de messages
        self._add_message("📊 STATISTIQUES FINALES:", 'title')
        self._add_message(f"   🏆 Score final : {hero.score}", 'info')
        self._add_message(f"   👹 Monstres tués : {hero.monsters_defeated}", 'info')
        self._add_message(f"   👣 Mouvements : {hero.move_count}", 'info')
        
        # Popup de game over
        messagebox.showinfo(
            "💀 Game Over",
            f"Vous êtes mort !\n\n"
            f"📊 Score final : {hero.score}\n"
            f"👹 Monstres tués : {hero.monsters_defeated}\n"
            f"👣 Mouvements : {hero.move_count}"
        )
    
    def show_victory(self, hero):
        """Affiche l'écran de victoire (SANS popup - juste dans la zone de texte)"""
        self._add_message("\n🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉", 'victory')
        self._add_message("🏆 VICTOIRE ! Vous avez atteint l'arrivée ! 🏆", 'victory')
        self._add_message("🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉\n", 'victory')
        
        # Afficher les statistiques finales dans la zone de messages
        self._add_message("📊 STATISTIQUES FINALES:", 'title')
        self._add_message(f"   🏆 Score final : {hero.score}", 'success')
        self._add_message(f"   👹 Monstres tués : {hero.monsters_defeated}", 'info')
        self._add_message(f"   👣 Mouvements : {hero.move_count}", 'info')
    
    def show_goodbye(self):
        """Message d'au revoir"""
        self._add_message("👋 Au revoir ! Merci d'avoir joué !", 'info')
    
    def show_new_record(self, old_record):
        """Affiche un nouveau record"""
        self._add_message("\n🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆", 'success')
        self._add_message("🏆 NOUVEAU RECORD ÉTABLI ! 🏆", 'success')
        self._add_message(f"📈 Ancien record battu : {old_record} points", 'success')
        self._add_message("🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆🎆\n", 'success')
        
        # Attendre pour que le message s'affiche bien
        import time
        time.sleep(0.2)
        
        messagebox.showinfo("🏆 Nouveau Record !", f"Félicitations !\nAncien record battu : {old_record} points")
    
    def show_current_best(self, best_score):
        """Affiche le meilleur score actuel"""
        self._add_message("\n🏅 HIGHSCORE ACTUEL À BATTRE:", 'warning')
        self._add_message(f"🎯 Meilleur score : {best_score} points", 'warning')
        self._add_message("💪 Essayez de faire mieux la prochaine fois !\n", 'warning')
        
        # Attendre pour que le message s'affiche bien
        import time
        time.sleep(0.2)
    
    def show_farewell(self):
        """Message d'adieu final avec popup de victoire finale"""
        self._add_message("🎮 Merci d'avoir joué à AVENTURIER !", 'success')
        
        # MAINTENANT on affiche la popup de victoire (après les highscores)
        messagebox.showinfo(
            "🎉 Partie terminée !",
            "Félicitations !\n\n"
            "Consultez le journal pour voir vos statistiques\n"
            "et vos highscores !"
        )
        
        self._add_message("👋 Fermeture dans 10 secondes ou fermez manuellement...", 'info')
        
        # Attendre 10 secondes pour laisser le temps de lire les highscores
        self.root.after(10000, self.root.destroy)


if __name__ == "__main__":
    print("ATTENTION: Ce fichier contient l'interface graphique du jeu.")
    print("Pour lancer le jeu, exécutez : python controller.py")