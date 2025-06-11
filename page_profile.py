import customtkinter as ctk
from extract import extraire_infos
import os
import json

def update_profile(user_data, data_niveaux, path_utilisateur, label_points, label_niveaux, progress_bar):
    label_points.configure(text=f"Points: {user_data['points_totaux']}")
    niveau_actuel = user_data.get("niveau", 0)
    if data_niveaux and niveau_actuel < len(data_niveaux) - 1 and user_data["points_totaux"] >= data_niveaux[niveau_actuel].points_requis:
        user_data["niveau"] = niveau_actuel + 1
        if label_niveaux is not None:
            label_niveaux.configure(text=f"Niveau: {user_data['niveau']}")
    elif data_niveaux and niveau_actuel > 0 and user_data["points_totaux"] < data_niveaux[niveau_actuel - 1].points_requis:
        user_data["niveau"] = niveau_actuel - 1
        if label_niveaux is not None:
            label_niveaux.configure(text=f"Niveau: {user_data['niveau']}")

    progress_bar.set(min(user_data["points_totaux"] / data_niveaux[niveau_actuel].points_requis, 1))
    
    if path_utilisateur.endswith(".json"):
        
        try:
            with open(path_utilisateur, "r", encoding="utf-8") as f:
                all_data = json.load(f)
        except:
            all_data = []
        for ud in all_data:
            if ud["nom"] == user_data["nom"]:
                ud["points_totaux"] = user_data["points_totaux"]
                ud["niveau"] = user_data["niveau"]
        
        with open(path_utilisateur, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)

def load_profile_page(parent, user_data):
    frame_profil = ctk.CTkFrame(parent)
    frame_profil.pack(fill="both", expand=True, padx=10, pady=10)

    # Nom de l'utilisateur en haut, centré
    label_nom = ctk.CTkLabel(frame_profil, text=user_data["nom"], font=("Arial", 18))
    label_nom.pack(pady=10)

    # Barre de progression et infos niveau/points
    gauge_frame = ctk.CTkFrame(frame_profil)
    gauge_frame.pack(pady=10)
    label_points = ctk.CTkLabel(gauge_frame, text=f"Points: {user_data['points_totaux']}")
    label_points.pack(side="left", padx=5)

    progress_bar = ctk.CTkProgressBar(gauge_frame, width=200)
    progress_bar.pack(side="left", padx=5)
    progress_bar.set(min(user_data['points_totaux'] / 100, 1))

    label_niveaux = ctk.CTkLabel(gauge_frame, text=f"Niveau: {user_data['niveau']}")
    label_niveaux.pack(side="left", padx=5)

    # Liste d’exercices
    data = extraire_infos()
    exercices = data.get("exercices", [])
    frame_exos = ctk.CTkFrame(frame_profil)
    frame_exos.pack(pady=10)
    ctk.CTkLabel(frame_exos, text="Exercices disponibles :").pack()
    
    def select_exercise(exo):
        path_utilisateur = f"Calisthenics_app/data/utilisateurs/{user_data['nom']}.json"
        if not exo.points_par_repetition:
            return
        if not user_data.get("points_totaux"):
            user_data["points_totaux"] = 0
        if not path_utilisateur or not exo:
            return

        user_data["points_totaux"] += exo.points_par_repetition
        update_profile(
            user_data,
            data.get("niveaux", []),
            f"Calisthenics_app/data/utilisateurs/{user_data['nom']}.json",
            label_points,
            label_niveaux,
            progress_bar
        )

    for exo in exercices:
        ctk.CTkButton(frame_exos, text=exo.nom, command=lambda e=exo: select_exercise(e)).pack(pady=2)

    # Bouton activer malus en bas
    ctk.CTkButton(frame_profil, text="Activer Malus",
                  command=lambda: show_malus_modal(frame_profil, user_data, data, label_points, progress_bar, label_niveaux)).pack(side="bottom", pady=10)


def show_malus_modal(parent, user_data, data, label_points, progress_bar, label_niveaux):
    malus_window = ctk.CTkToplevel(parent)
    malus_window.title("Appliquer un Malus")
    malus_window.geometry("300x200")
    malus_window.grab_set()
    ctk.CTkLabel(malus_window, text="Sélectionnez un malus :").pack(padx=10, pady=5)
    liste_malus = [m.nom for m in data.get("malus", [])]
    combo_malus = ctk.CTkComboBox(malus_window, values=liste_malus)
    combo_malus.pack(padx=10, pady=5)

    def appliquer_malus():
        selection = combo_malus.get()
        for m in data.get("malus", []):
            if m.nom == selection:
                user_data["points_totaux"] -= m.points_perdus
        update_profile(
            user_data,
            data.get("niveaux", []),
            f"Calisthenics_app/data/utilisateurs/{user_data['nom']}.json",
            label_points,
            label_niveaux,
            progress_bar
        )
        malus_window.destroy()

    ctk.CTkButton(malus_window, text="Appliquer", command=appliquer_malus).pack(pady=10)
