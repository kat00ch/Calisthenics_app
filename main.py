import customtkinter as ctk
from page_users import load_users_page
from page_profile import load_profile_page
from page_instructions import load_instructions_page

window = ctk.CTk()
window.title("Application de gestion d'exercices")
window.geometry("550x700")

main_frame = ctk.CTkFrame(window)
main_frame.pack(fill="both", expand=True)

selected_user = None

def set_selected_user(user_data):
    global selected_user
    selected_user = user_data
    print(f"Utilisateur sélectionné : {user_data['nom']}")

def show_users():
    for widget in main_frame.winfo_children():
        widget.destroy()
    load_users_page(main_frame, set_selected_user)

def show_profile():
    for widget in main_frame.winfo_children():
        widget.destroy()
    if selected_user:
        load_profile_page(main_frame, selected_user)
    else:
        ctk.CTkLabel(main_frame, text="Aucun utilisateur sélectionné").pack()

def show_instructions():
    for widget in main_frame.winfo_children():
        widget.destroy()
    load_instructions_page(main_frame)

show_users()

ctk.CTkButton(window, text="Gérer Utilisateurs", command=show_users).pack(side="left", padx=10, pady=10)
ctk.CTkButton(window, text="Voir Profil", command=show_profile).pack(side="left", padx=10, pady=10)
ctk.CTkButton(window, text="Instructions", command=show_instructions).pack(side="left", padx=10, pady=10)

window.mainloop()