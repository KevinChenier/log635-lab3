# Google Text to Speech API
from gtts import gTTS
import os

# Library to play an mp3 using python
from playsound import playsound

class Tts:

    Language = ''
    def __init__(self, language):
        self.Language = language

    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    def playaudio(self, text):
        file = gTTS(text=text, lang=self.Language, slow=False)
        # Saving the converted audio in a mp3 file
        file.save('speech.mp3')
        # Playing the converted file
        playsound('speech.mp3', True)
        os.remove('speech.mp3')

