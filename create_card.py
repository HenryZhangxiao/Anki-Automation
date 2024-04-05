import json
import genanki

#Initialize Model
my_model = genanki.Model(
  1,
  'Default',
  fields=[
    {'name': 'Kana'},
    {'name': 'Kanji'},
    {'name': 'Example Sentence'},
    {'name': 'English Translation'},
    {'name': 'English Example Sentence'},
  ],
  templates=[
    {
      'name': 'Card',
      'qfmt': '{{Kana}}<br>{{Kanji}}',
      'afmt': '<hr id="es">{{Example Sentence}}<hr id="et">{{English Translation}}<hr id="ees">{{English Example Sentence}}',
    }
  ])


'''
Takes in a json file name and reads the information. It then stores the information in a list.

Parameters: file (String)
'''
def read_json(file):
  #Open JSON file
  f = open(file, encoding='utf8')
  f_loaded = json.load(f)
  card_info_tuple = ()
  card_list = []

  #Iterate through JSON file and get all fields
  for i in range(len(f_loaded)):
    kana = f_loaded[i][0]
    kanji = f_loaded[i][1]
    example_sentence = f_loaded[i][2]
    english_translation = f_loaded[i][3]
    english_example_sentence = f_loaded[i][4]

    #Create card_info_tuple used to store fields
    card_info_tuple = (kana, kanji, example_sentence, english_translation, english_example_sentence)

    #Add card_info_tuple to the card_list
    if card_info_tuple not in card_list:
      card_list.append(card_info_tuple) 

  return card_list

'''
Iterates through a list of cards, creates a card and adds it to an existing deck. 

Parameters: card_list (List), deck (genanki.Deck)
'''
def create_card(card_list, deck: genanki.Deck):
  #Iterate through the card list and add card to deck
  for card in card_list:
    note = genanki.Note(model= my_model, fields=[card[0], card[1], card[2], card[3], card[4]])

    #Add card to deck
    deck.add_note(note)

'''
Main method
'''
def main():
  card_list1 = read_json("data.json")
  deck1 = genanki.Deck(1, "Deck1")
  create_card(card_list1, deck1)
  genanki.Package(deck1).write_to_file("Deck1.apkg")

if __name__ == "__main__":
    main()