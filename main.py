# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from pynput import keyboard

from bot import *
from board import *

if __name__ == '__main__':
    board = board(10)
    bot = Bot('fr', board)
    bot.move()
    bot.move()
    bot.move()