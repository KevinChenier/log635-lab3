# Google Text to Speech API
from gtts import gTTS
import os

# Library to play an mp3 using python
from playsound import playsound

class Bot:

    Language = ''
    def __init__(self, language):
        self.Language = language

    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    def speak(self, text):
        self.Language
        file = gTTS(text=text, lang=self.Language, slow=False)
        # Saving the converted audio in a mp3 file
        file.save('audio/speech.mp3')
        # Playing the converted file
        playsound('audio/speech.mp3', True)
        os.remove('audio/speech.mp3')

