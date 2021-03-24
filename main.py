# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Ressources.SyntheseVocaleSimple.tts import *
import os.path
#Path to text file containing starting infrmations


def readTextFile(path):
    return open(path)

def getStartingInformations():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'informations.txt')
    startingInformations = readTextFile(my_file)
    text = startingInformations.read()
    print(text)
    return text

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bot = Bot('en')
    
    
   
    bot.speak(getStartingInformations())
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
