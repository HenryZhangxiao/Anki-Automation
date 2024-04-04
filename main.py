import tkinter as tk
from tkinter import filedialog
import create_card
import genanki

file_path = ""

def select_file():
    file_path = filedialog.askopenfilename()
    #Run google ocr

def create_deck():
    deck = genanki.Deck
    create_card.create_card(create_card.read_json(file_path), deck)
    genanki.Package(deck).write_to_file("Deck1")

def main():
    root = tk.Tk()
    root.title("Anki Deck Generator")

    root.geometry("1000x500")

    title_label = tk.Label(root, text="Anki Deck Generator", font=("Helvetica", 16))
    title_label.pack(pady=10)

    select_button = tk.Button(root, text="Select File", command=select_file)
    select_button.pack(pady=5)

    create_button = tk.Button(root, text="Create Deck", command=create_deck)
    create_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
