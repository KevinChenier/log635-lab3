from character import *
from weapon import *

class Room:

    def __init__(self, name, character, weapon, is_crime_room):
        self.name = name
        self.character = character
        self.weapon = weapon
        self.is_crime_room = is_crime_room

    def get_name(self):
        return self.name

    def get_character(self):
        return self.character

    def get_weapon(self):
        return self.weapon

    def get_is_crime_room(self):
        return self.is_crime_room