import json
from random import randrange
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
        if numberOfRooms > 0 & numberOfRooms <= 10:
            # print(number)

            SallesJeux = []

            salles = ["Cuisine", "Salle de balle", "Salon", "SalleAManger", "Cave", "Bureau", "Bibliotheque", "Veranda", "Hall", "Studio"]
            pion_couleur = ["rouge", "mauve", "bleu", "vert", "jaune", "blanc"]
            weapons = ["Poignard", "Corde", "Revolver", "Chandelier", "Clé anglaise", "Matraque"]

            # Informations
            heure_crime = randrange(24)
            killer = pion_couleur[randrange(6)]
            is_crime_weapon = weapons[randrange(6)]

            print("Le tueur est ", killer)
            print("L'arme du crime est ", is_crime_weapon)

            # Construction du tableau de jeu
            data = {};
            data['informations'] = []
            data['informations'].append({
                'crime_hour': heure_crime
            })
            data['informations'].append({
                'crime_injury': weapons[randrange(6)]
            })

            numeroPieceUtiliser = []
            # On ajoute les salles aleatoirement que l'on va utiliser
            for x in range(numberOfRooms):
                ok = False
                while not ok:
                    test = randrange(10)
                    if test not in numeroPieceUtiliser:
                        numeroPieceUtiliser.append(salles[test])
                        ok = True

            crime_room = numeroPieceUtiliser[randrange(numberOfRooms)]
            weapon_index = 0
            # for y in pionCouleur:

            data['SalleDeJeu'] = []

            i = 0
            while i < 6:
                position = randrange(numberOfRooms)
                positionPionOneHour = randrange(numberOfRooms)
                positionWeaponOneHour = randrange(numberOfRooms)

                is_killer = False
                if killer is pion_couleur[i]:
                    is_killer = True

                isCrimeWeapon = False
                if is_crime_weapon is weapons[weapon_index]:
                    isCrimeWeapon = True

                isCrimeRoom = False
                if salles[position] is crime_room:
                    isCrimeRoom = True

                data['SalleDeJeu'].append({
                    'name': salles[position],
                    'character': {
                        'name': pion_couleur[i],
                        'location': salles[position],
                        'location_one_hour_after_crime': salles[positionPionOneHour],
                        'isKiller': is_killer
                    },
                    'weapon': {
                        'name': weapons[weapon_index],
                        'location': salles[position],
                        'location_one_hour_after_crime': salles[positionWeaponOneHour],
                        'is_crime_weapon': isCrimeWeapon
                    },
                    'is_crime_room': isCrimeRoom
                })

                character = Character(pion_couleur[i], salles[position], salles[positionPionOneHour], is_killer)
                weapon = Weapon(weapons[weapon_index], salles[position], salles[positionWeaponOneHour], isCrimeWeapon)
                room = Room(salles[position], character, weapon, isCrimeRoom)

                self.characters.append(character)
                self.weapons.append(weapon)
                self.rooms.append(room)

                # print(weapons[weaponIndex]) --- DEBUG ---

                weapon_index += 1
                i += 1

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