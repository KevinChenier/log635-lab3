from bot import *
from board import *

class Gameplay:

    def __init__(self):
        self.board = Board(10)
        self.bot = Bot('fr', self.board)

    def loop(self):
        while True:
            self.bot.move()

    def play(self):
        while True:
            self.bot.move()
            self.bot.memorize(self.bot.current_room.get_character().get_name() + ' est dans ' + self.bot.current_room.get_name())
            self.bot.memorize(self.bot.current_room.get_weapon().get_name() + ' est dans ' + self.bot.current_room.get_name())