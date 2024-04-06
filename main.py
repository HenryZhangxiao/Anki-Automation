#!/usr/bin/env python

# Importing necessary libraries
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import create_card
import genanki
import helpers
import os

# Global variables initialization
file_paths = [] 
deck_created = False
decks_created = []
saved_decks_folder = "saved_decks"  

# Function to select multiple files
def select_files():
    global file_paths
    global create_button
    # Check if deck has been created previously, if yes, reset status_label
    if status_label.cget("text") == "Deck created!":
        status_label.config(text="", foreground="#fff", font=("Helvetica", 16))
    # Open file dialog to select multiple files
    files = filedialog.askopenfilenames()
    if files:
        # Store selected file paths
        file_paths = list(files)
        # Update directory_label with selected file paths
        directory_label.config(text="Current directory: " + ", ".join(file_paths), foreground="#fff", font=("Helvetica", 14, "bold"))
        # List existing .apkg files
        list_existing_apkg_files()
        # Enable create_button
        create_button.config(state="normal")

# Function to create a deck from selected files
def create_deck():
    global file_paths
    global deck_created
    global delete_deck_button
    # Check if no files are selected
    if not file_paths:
        return

    # Check if deck has already been created
    if status_label.cget("text") == "Deck created!":
        messagebox.showerror("Error", "A deck has already been created. Please select files again.")
        return

    # Get user input for deck name
    deck_name = simpledialog.askstring("Input", "Enter the name for the deck file:")
    if deck_name is None:
        return

    # Check if a file with the same name already exists in the directory
    if os.path.exists(os.path.join(saved_decks_folder, deck_name + ".apkg")):
        messagebox.showerror("Error", "A file with the same name already exists in the directory.")
        return

    # Initialize a deck object
    deck = genanki.Deck(1, deck_name)

    # Iterate over selected file paths to create cards
    for file_path in file_paths:
        # Run Google OCR on each file
        helpers.google_document_ai(file_path)
        # Create cards from the extracted text
        create_card.create_card(create_card.read_json('data.json'), deck)

    # Write the deck to a .apkg file
    genanki.Package(deck).write_to_file(os.path.join(saved_decks_folder, deck_name + ".apkg"))

    # Update status_label and decks_created list
    status_label.config(text="Deck created!", foreground="green", font=("Helvetica", 16, "bold"))
    decks_created.append(deck_name)
    # List existing .apkg files
    list_existing_apkg_files()
    # Update deck_created flag and enable delete_deck_button
    deck_created = True
    delete_deck_button.config(state="normal")

# Function to delete selected deck files
def delete_deck():
    global decks_created
    global deck_created
    # Check if deck has been created
    if not deck_created:
        messagebox.showerror("Error", "Please create a deck before deleting.")
        return

    # Open file dialog to select files to delete
    files = filedialog.askopenfilenames()
    if files:
        # Iterate over selected files
        for file_path in files:
            # Extract the deck name from file path
            selected_deck = os.path.splitext(os.path.basename(file_path))[0]
            # Check if selected deck exists in decks_created list
            if selected_deck in decks_created:
                decks_created.remove(selected_deck)  # Remove from decks_created list
                list_existing_apkg_files()  # Update existing files label

                # Delete corresponding .apkg file
                apkg_file = os.path.join(saved_decks_folder, selected_deck + ".apkg")
                if os.path.exists(apkg_file):
                    os.remove(apkg_file)
            else:
                messagebox.showerror("Error", "The specified deck does not exist.")

# Function to list existing .apkg files
def list_existing_apkg_files():
    existing_files_label.config(text="Decks created: " + ", ".join(decks_created), foreground="#fff", font=("Helvetica", 14, "bold"))

# Main function to create the GUI
def main():
    global root
    global create_button
    global delete_deck_button

    # Initialize the Tkinter window
    root = tk.Tk()
    root.title("Anki Deck Generator")
    root.geometry("1000x500")
    root.configure(background="black")

    # Title label
    title_label = tk.Label(root, text="Anki Deck Generator", font=("Helvetica", 24, "bold"), bg="gray", fg="#fff", padx=10, pady=10)
    title_label.place(relx=0.5, rely=0.1, anchor="center")

    # Styling for buttons
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Rounded.TButton', font=('Helvetica', 14, 'bold'), foreground="#fff", background="#007bff", relief=tk.FLAT, borderwidth=0, padding=10)

    # Select button
    select_button = ttk.Button(root, text="Select", command=select_files, style='Rounded.TButton')
    select_button.place(relx=0.3, rely=0.3, anchor="center")

    # Create deck button
    create_button = ttk.Button(root, text="Create Deck", command=create_deck, style='Rounded.TButton', state="disabled")
    create_button.place(relx=0.7, rely=0.3, anchor="center")

    # Delete deck button
    delete_deck_button = ttk.Button(root, text="Delete Deck", command=delete_deck, style='Rounded.TButton', state="disabled")
    delete_deck_button.place(relx=0.5, rely=0.5, anchor="center")

    # Directory label
    global directory_label
    directory_label = tk.Label(root, text="Current directory: ", font=('Helvetica', 14, "bold"), background="black", foreground="#fff")
    directory_label.place(relx=0.5, rely=0.7, anchor="center")

    # Status label
    global status_label
    status_label = tk.Label(root, text="", font=('Helvetica', 16), background="black", foreground="#fff")
    status_label.place(relx=0.5, rely=0.8, anchor="center")

    # Existing files label
    global existing_files_label
    existing_files_label = tk.Label(root, text="", font=('Helvetica', 14), background="black", foreground="#fff")
    existing_files_label.place(relx=0.5, rely=0.9, anchor="center")

    # Start the Tkinter event loop
    root.mainloop()

# Check if the script is being run directly
if __name__ == "__main__":
    main()
