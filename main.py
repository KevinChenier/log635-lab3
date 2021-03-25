# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from bot import *

if __name__ == '__main__':
    bot = Bot('en')

    bot.listenMicrophone()

    bot.listenConsole()

    text = bot.readFileText("informations.txt")
    bot.speak(text)

