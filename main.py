# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from pynput import keyboard

from bot import *
from board import *
from gameplay import *

if __name__ == '__main__':
    board = Board(10)
    gameplay = Gameplay()
    bot = Bot('fr', board)
    
    while True:
        gameplay.play()