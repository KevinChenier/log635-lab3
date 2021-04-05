import json
from random import randrange
import random
from room import *
from weapon import *
from character import *
from types import SimpleNamespace

import jsbeautifier

class board:

    characters = []
    weapons = []
    rooms = []

    def __init__(self, numberOfRooms):
        if numberOfRooms > 0 & numberOfRooms <= 6:
            # print(number)

            salles = ["Cuisine", "Garage", "Salon", "Cave", "Bureau", "Studio"]
            pions_couleur = ["Rouge", "Mauve", "Bleu", "Vert", "Jaune", "Blanc"]
            weapons = ["Poignard", "Corde", "Revolver", "Chandelier", "Poison", "Matraque"]

            random.shuffle(salles)
            random.shuffle(pions_couleur)
            random.shuffle(weapons)

            # Informations
            heure_crime = randrange(24)
            killer = pions_couleur[randrange(numberOfRooms)]
            crime_weapon = weapons[randrange(numberOfRooms)]
            crime_room = salles[randrange(numberOfRooms)]

            print("Le tueur est ", killer)
            print("L'arme du crime est ", crime_weapon)

            # Construction du tableau de jeu
            data = {};
            data['informations'] = []
            data['informations'].append({
                'crime_hour': heure_crime
            })
            data['informations'].append({
                'crime_injury': crime_weapon
            })

            data['SalleDeJeu'] = []

            for i in range(numberOfRooms):
                positionPionOneHour = randrange(numberOfRooms)
                positionWeaponOneHour = randrange(numberOfRooms)

                is_killer = True if killer is pions_couleur[i] else False
                is_crime_weapon = True if crime_weapon is weapons[i] else False
                is_crime_room = True if crime_room is salles[i] else False

                data['SalleDeJeu'].append({
                    'name': salles[i],
                    'character': {
                        'name': pions_couleur[i],
                        'location': salles[i],
                        'location_one_hour_after_crime': salles[positionPionOneHour],
                        'isKiller': is_killer
                    },
                    'weapon': {
                        'name': weapons[i],
                        'location': salles[i],
                        'location_one_hour_after_crime': salles[positionWeaponOneHour],
                        'is_crime_weapon': is_crime_weapon
                    },
                    'is_crime_room': is_crime_room
                })

                character = Character(pions_couleur[i], salles[i], salles[positionPionOneHour], is_killer)
                weapon = Weapon(weapons[i], salles[i], salles[positionWeaponOneHour], crime_weapon)
                room = Room(salles[i], character, weapon, is_crime_room)

                self.characters.append(character)
                self.weapons.append(weapon)
                self.rooms.append(room)

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