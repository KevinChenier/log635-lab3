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
            self.bot.searchRoom(1)
            
            
