import customtkinter as ctk

def load_instructions_page(parent):
    frame_instructions = ctk.CTkFrame(parent)
    frame_instructions.pack(padx=20, pady=5)
    ctk.CTkLabel(frame_instructions, text="Instructions des exercices").pack()
    # ...plus tard, afficher le détail d’un exercice...
