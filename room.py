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