import os
import json
import datetime
import customtkinter as ctk
from extract import creer_joueur

def load_users_page(parent, on_select_user):
    afficher_utilisateurs(parent, on_select_user)
    bouton_nouveau_joueur = ctk.CTkButton(
        parent,
        text="Nouveau Joueur",
        command=lambda: ouvrir_creation_joueur(parent, on_select_user, bouton_nouveau_joueur)
    )
    bouton_nouveau_joueur.pack(pady=5)

def afficher_utilisateurs(parent, on_select_user):
    frame_liste_utilisateurs = ctk.CTkFrame(parent)
    frame_liste_utilisateurs.pack(pady=5)

    if not os.path.exists("data/utilisateurs"):
        os.makedirs("data/utilisateurs")

    all_users_data = []
    for user_file in os.listdir("data/utilisateurs"):
        if user_file.endswith(".json"):
            with open(os.path.join("data/utilisateurs", user_file), "r", encoding="utf-8") as f:
                try:
                    data_utilisateurs = json.load(f)
                except:
                    data_utilisateurs = []
            for user_data in data_utilisateurs:
                all_users_data.append(user_data)

    if not all_users_data:
        ctk.CTkLabel(frame_liste_utilisateurs, text="Aucun utilisateur trouvé").pack()
        return

    for user_data in all_users_data:
        frame_user = ctk.CTkFrame(frame_liste_utilisateurs)
        frame_user.pack(pady=5)

        texte = f"{user_data['nom']} - Niveau: {user_data['niveau']} - Points: {user_data['points_totaux']}"
        ctk.CTkLabel(frame_user, text=texte).pack(side="top", padx=5, pady=5)

        def select_this_user(u=user_data):
            on_select_user(u)
        ctk.CTkButton(frame_user, text="Sélectionner", command=select_this_user).pack()

def ouvrir_creation_joueur(parent, on_select_user, bouton_nouveau_joueur):
    bouton_nouveau_joueur.configure(state="disabled")
    frame_nouveau = ctk.CTkFrame(parent)
    frame_nouveau.pack(pady=5)

    ctk.CTkLabel(frame_nouveau, text="Nom du joueur :").pack()
    entry_nom = ctk.CTkEntry(frame_nouveau)
    entry_nom.pack(pady=5)

    def creer_et_sauver_joueur():
        id_joueur = f"user_{len(os.listdir('data/utilisateurs')) + 1}"
        nom_joueur = entry_nom.get()
        date_debut = datetime.datetime.now().strftime("%Y-%m-%d")
        nouveau_joueur = creer_joueur(nom_joueur, id_joueur, date_debut)
        path_utilisateur = f"data/utilisateurs/{nom_joueur}.json"

        if not os.path.exists(path_utilisateur):
            data_utilisateurs = []
        else:
            with open(path_utilisateur, "r", encoding="utf-8") as f:
                try:
                    data_utilisateurs = json.load(f)
                except:
                    data_utilisateurs = []

        data_utilisateurs.append(nouveau_joueur.__dict__)
        with open(path_utilisateur, "w", encoding="utf-8") as f:
            json.dump(data_utilisateurs, f, ensure_ascii=False, indent=2)

        on_select_user(nouveau_joueur.__dict__)
        for widget in parent.winfo_children():
            widget.destroy()
        load_users_page(parent, on_select_user)
        bouton_nouveau_joueur.configure(state="normal")

    ctk.CTkButton(frame_nouveau, text="Créer", command=creer_et_sauver_joueur).pack(pady=5)