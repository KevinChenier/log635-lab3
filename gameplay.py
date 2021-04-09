from bot import *
from board import *


class Gameplay:

    def __init__(self):
        self.board = Board(10)
        self.bot = Bot('fr', self.board)

    def loop(self):
        while self.bot.crime_solved is False:
            self.bot.investigate()
