import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import create_card
import genanki
import helpers
import os

file_paths = [] 
deck_created = False
decks_created = []
saved_decks_folder = "saved_decks"  

def select_files():
    global file_paths
    global create_button
    if status_label.cget("text") == "Deck created!":
        status_label.config(text="", foreground="#fff", font=("Helvetica", 16))
    files = filedialog.askopenfilenames()
    if files:
        file_paths = list(files)
        directory_label.config(text="Current directory: " + ", ".join(file_paths), foreground="#fff", font=("Helvetica", 14, "bold"))
        list_existing_apkg_files()
        create_button.config(state="normal")

def create_deck():
    #Run google ocr
    helpers.google_document_ai(file_path)
    deck = genanki.Deck
    create_card.create_card(create_card.read_json('data.json'), deck)
    # create_card.create_card(create_card.read_json(file_path), deck)
    genanki.Package(deck).write_to_file("NewDeck.apkg")

def main():
    global root
    global create_button
    global delete_deck_button

    root = tk.Tk()
    root.title("Anki Deck Generator")
    root.geometry("1000x500")
    root.configure(background="black")

    title_label = tk.Label(root, text="Anki Deck Generator", font=("Helvetica", 24, "bold"), bg="gray", fg="#fff", padx=10, pady=10)
    title_label.place(relx=0.5, rely=0.1, anchor="center")

    style = ttk.Style()

    style.theme_use('clam')

    style.configure('Rounded.TButton', font=('Helvetica', 14, 'bold'), foreground="#fff", background="#007bff", relief=tk.FLAT, borderwidth=0, padding=10)

    select_button = ttk.Button(root, text="Select", command=select_files, style='Rounded.TButton')
    select_button.place(relx=0.3, rely=0.3, anchor="center")

    create_button = ttk.Button(root, text="Create Deck", command=create_deck, style='Rounded.TButton', state="disabled")
    create_button.place(relx=0.7, rely=0.3, anchor="center")

    delete_deck_button = ttk.Button(root, text="Delete Deck", command=delete_deck, style='Rounded.TButton', state="disabled")
    delete_deck_button.place(relx=0.5, rely=0.5, anchor="center")

    global directory_label
    directory_label = tk.Label(root, text="Current directory: ", font=('Helvetica', 14, "bold"), background="black", foreground="#fff")
    directory_label.place(relx=0.5, rely=0.7, anchor="center")

    global status_label
    status_label = tk.Label(root, text="", font=('Helvetica', 16), background="black", foreground="#fff")
    status_label.place(relx=0.5, rely=0.8, anchor="center")

    global existing_files_label
    existing_files_label = tk.Label(root, text="", font=('Helvetica', 14), background="black", foreground="#fff")
    existing_files_label.place(relx=0.5, rely=0.9, anchor="center")

    root.mainloop()

if __name__ == "__main__":
    main()
