import json
from random import randrange

import jsbeautifier


class board:

    def __init__(self, numberOfRooms):

        if numberOfRooms > 0 & numberOfRooms <= 10:
            # print(number)

            SallesJeux = []

            # Informations
            heureDuCrime = randrange(24)
            Salles = ["Cuisine", "Salle de ball", "Salon", "SalleAManger",
                      "Cave", "Bureau", "Bibliotheque", "Veranda", "Hall", "Studio"]

            pionCouleur = ["rouge", "mauve", "bleu", "vert", "jaune", "blanc"]
            weapons = ["Poignard", "Corde", "Revolver", "Chandelier", "Clé anglaise", "Matraque"]

            Killer = pionCouleur[randrange(6)]
            is_crime_weapon = weapons[randrange(6)]


            print(Killer)
            print(is_crime_weapon)
            print('***********************************')

            # Construction du tableau de jeu
            data = {};
            data['informations'] = []
            data['informations'].append({
                'crime_hour': heureDuCrime
            })
            data['informations'].append({
                'crime_injury': weapons[randrange(6)]
            })

            # On ajoute les salles aleatoirement que l'on va utiliser
            numeroPieceUtiliser = []
            for x in range(numberOfRooms):
                ok = False
                while not ok:
                    test = randrange(10)
                    if test not in numeroPieceUtiliser:
                        numeroPieceUtiliser.append(Salles[test])
                        ok = True

            crimeRoom = numeroPieceUtiliser[randrange(numberOfRooms)]
            weaponIndex = 0
            # for y in pionCouleur:

            data['SalleDeJeu'] = []

            i = 0
            while i < 5:
                position = randrange(numberOfRooms)
                positionPionOneHour = randrange(numberOfRooms)
                positionWeaponOneHour = randrange(numberOfRooms)

                iskiller = False
                if Killer is pionCouleur[i]:
                    iskiller = True

                isCrimeWeapon = False
                if is_crime_weapon is weapons[weaponIndex]:
                    isCrimeWeapon = True

                isCrimeRoom = False
                if Salles[position] is crimeRoom:
                    isCrimeRoom = True


                data['SalleDeJeu'].append({
                    'name': Salles[position],
                    'character': {
                        'name': pionCouleur[i],
                        'location': Salles[position],
                        'location_one_hour_after_crime': Salles[positionPionOneHour],
                        'isKiller': iskiller
                    },
                    'weapon': {
                        'name': weapons[weaponIndex],
                        'location': Salles[position],
                        'location_one_hour_after_crime': Salles[positionWeaponOneHour],
                        'is_crime_weapon': isCrimeWeapon
                    },
                    'is_crime_room': isCrimeRoom
                })

                print(weapons[weaponIndex])
                weaponIndex += 1
                i += 1


            with open('game_board.json', 'w') as outfile:
                json.dump(data, outfile)
