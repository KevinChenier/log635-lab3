import json
from random import randrange
import random
from room import *
from weapon import *
from character import *
from types import SimpleNamespace

import jsbeautifier

class Board:

    characters = []
    weapons = []
    rooms = []

    def __init__(self, numberOfRooms):
        if numberOfRooms > 0 & numberOfRooms <= 10:
            # print(number)

            salles = ["Cuisine", "Garage", "Salon", "Cave", "Bureau", "Studio", "Lounge", "Toilette", "Corridor", "Entrée"]
            characters = ["Rouge", "Mauve", "Bleu", "Vert", "Jaune", "Blanc", "Violet", "Turquoise", "Noir", "Rose"]
            weapons = ["Poignard", "Corde", "Revolver", "Chandelier", "Poison", "Matraque", "Couteau", "Verre", "Shotgun", "Clavier"]

            # Rearrange lists
            random.shuffle(salles)
            random.shuffle(characters)
            random.shuffle(weapons)

            # Only take the elements necessary
            salles = salles[:numberOfRooms]
            characters = characters[:numberOfRooms]
            weapons = weapons[:numberOfRooms]

            # Informations
            heure_crime = randrange(24)
            crime_room = random.choice(salles)
            crime_weapon = random.choice(weapons)
            self.set_crime_injury(crime_weapon)

            # Construction du tableau de jeu
            data = {};
            data['informations'] = []
            data['informations'].append({
                'crime_hour': heure_crime
            })
            data['informations'].append({
                'crime_injury': self.crime_injury
            })

            data['SalleDeJeu'] = []

            salles_character_one_hour = salles.copy()
            salles_weapon_during_crime = salles.copy()
            random.shuffle(salles_character_one_hour)
            random.shuffle(salles_weapon_during_crime)

            for i in range(numberOfRooms):

                is_killer = False
                is_crime_weapon = True if crime_weapon is weapons[i] else False
                is_crime_room = True if crime_room is salles[i] else False

                weapon = Weapon(weapons[i], salles[i], salles_weapon_during_crime[i], is_crime_weapon)

                # Determine le tueur:
                # Si la personne se trouvait dans une piece qui contient l'arme
                # qui a tué la victime une heure après le meurtre alors elle est suspecte
                if weapon.get_is_crime_weapon() and salles_character_one_hour[i] is weapon.get_location():
                    is_killer = True
                character = Character(characters[i], salles[i], salles_character_one_hour[i], is_killer)

                room = Room(salles[i], character, weapon, is_crime_room)

                data['SalleDeJeu'].append({
                    'name': salles[i],
                    'character': {
                        'name': characters[i],
                        'location': salles[i],
                        'location_one_hour_after_crime': salles_character_one_hour[i],
                        'isKiller': is_killer
                    },
                    'weapon': {
                        'name': weapons[i],
                        'location': salles[i],
                        'location_during_crime': salles_weapon_during_crime[i],
                        'is_crime_weapon': is_crime_weapon
                    },
                    'is_crime_room': is_crime_room
                })

                self.characters.append(character)
                self.weapons.append(weapon)
                self.rooms.append(room)
            # Add the known victim
            victim = Character('Alex', '?', '?', False)
            self.characters.append(victim)

            with open('game_board.json', 'w') as outfile:
                json.dump(data, outfile)

        print('*******************************************************')
        # Creation du fichier Room_facts

        dataW = {}
        dataW['room_facts'] = []

        with open('game_board.json') as json_file:
            dataR = json.load(json_file)
            for p in dataR['SalleDeJeu']:
                print(p['character']['name'] + ', est dans la salle: ' + p['character']['location'])
                print(p['weapon']['name'] + ', est dans la salle: ' + p['weapon']['location'])

                dataW['room_facts'].append({
                    'person_Location': p['character']['name'] + ', est dans la salle: ' + p['character']['location'],
                    'weapon_location': p['weapon']['name'] + ', est dans la salle: ' + p['weapon'][
                        'location']
                })

        with open('room_facts.json', 'w') as outfile:
            json.dump(dataW, outfile)

    def get_rooms(self):
        return self.rooms

    def get_weapons(self):
        return self.weapons

    def get_characters(self):
        return self.characters

    def get_rooms_string(self):
        rooms = []
        for room in self.rooms:
            rooms.append(room.get_name())
        return rooms

    def get_weapons_string(self):
        weapons = []
        for weapon in self.weapons:
            weapons.append(weapon.get_name())
        return weapons

    def get_characters_string(self):
        characters = []
        for character in self.characters:
            characters.append(character.get_name())
        return characters

    def get_rooms_all_string(self):
        rooms = []
        for room in self.rooms:
            rooms.append(room.get_name())
            rooms.append(room.get_name().lower())
        return rooms

    def get_weapons_all_string(self):
        weapons = []
        for weapon in self.weapons:
            weapons.append(weapon.get_name())
            weapons.append(weapon.get_name().lower())
        return weapons

    def get_characters_all_string(self):
        characters = []
        for character in self.characters:
            characters.append(character.get_name())
            characters.append(character.get_name().lower())
        return characters

    def set_crime_injury(self, weapon):
        if weapon in ("Revolver", "Shotgun"):
            self.crime_injury = "un trou à la poitrine"
        elif weapon in ("Poignard", "Verre", "Couteau"):
            self.crime_injury = "un plaie à la poitrine"
        elif weapon in ("Matraque", "Chandelier", "Clavier"):
            self.crime_injury = "le crâne fendu"
        elif weapon in ("Corde"):
            self.crime_injury = "une marque au cou"
        elif weapon in ("Poison"):
            self.crime_injury = "la peau verte"

    def get_crime_injury(self):
        return self.crime_injury
