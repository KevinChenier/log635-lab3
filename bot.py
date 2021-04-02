from random import random

import keyboard
from Ressources.SyntheseVocaleSimple.tts import *
from fileReader import *
import speech_recognition as sr
import random
from board import *

sr.__version__

class Bot:
    voice_recognizer = sr.Recognizer()
    micro = sr.Microphone()
    file_reader = FileReader()

    questions = "Ou suis-je?", \
                "Qu'est-ce que c'est?"

    response_user = ''
    info_to_analyze = ''

    WHO = ''
    HOW = ''
    WHERE = ''
    WHEN = ''

    def __init__(self, language, board):
        self.voice = Tts(language)
        self.board = board
        self.current_room = board.get_rooms()[0]

    def readFileText(self, fileName):
        return self.file_reader.getfiletext(fileName)

    def speak(self, textToSay):
        print(textToSay)
        self.voice.playaudio(textToSay)

    def memorize(self, text):
        self.info_to_analyze = text
        print('Texte memorisé:', text)

    # from https://realpython.com/python-speech-recognition/
    def recognize_speech_from_mic(self):
        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        with self.micro as source:
            self.voice_recognizer.adjust_for_ambient_noise(source)
            audio = self.voice_recognizer.listen(source)

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught,
        #     update the response object accordingly
        try:
            response["transcription"] = self.voice_recognizer.recognize_google(audio, language="fr-FR")
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        return response

    def listenMicrophone(self):
        self.speak("J'écoute...")
        response = self.recognize_speech_from_mic()
        transcription = response["transcription"]
        # show the user the transcription
        self.speak("Tu as dit: {}".format(transcription) + ", est-ce correcte?")

        if self.confirm():
            self.speak("Confirmé")
            return transcription
        else:
            self.speak("Recommençons,")
            self.listenMicrophone()

    def move(self):
        # self.speak("Appuyez sur une des touches suivantes")
        print("Appuyez sur [↑] [↓] [←] [→]")
        while True:  # making a loop

            if keyboard.is_pressed('up'):
                # print('You Pressed ↑ Key!')
                self.current_room = self.board.get_rooms()[0]
                break

            if keyboard.is_pressed('down'):
                # print('You Pressed ↓ Key!')
                length = len(self.board.get_rooms())
                self.current_room = self.board.get_rooms()[length-1]
                break

            if keyboard.is_pressed('left'):
                # print('You Pressed ← Key!')
                i = self.board.get_rooms().index(self.current_room)
                i = len(self.board.get_rooms()) - 1 if i == 0 else i - 1
                self.current_room = self.board.get_rooms()[i]
                break

            if keyboard.is_pressed('right'):
                i = self.board.get_rooms().index(self.current_room)
                i = 0 if i == len(self.board.get_rooms()) - 1 else i + 1
                self.current_room = self.board.get_rooms()[i]
                break

        self.speak("Je suis dans: " + self.current_room.get_name())

    def confirm(self):
        rand = random.choice([True, False])
        verdict = ''
        if rand:
            verdict = self.listenConsole()
        else:
            print("Confirmez par voix...")
            response = self.recognize_speech_from_mic()
            verdict = response["transcription"]

        return verdict in ('yes', 'oui', '1', 'true', 'vrai', 'v')

    def listenConsole(self):
        print("Entrez votre texte: ")
        user_input = input()
        self.speak("Vous avez écrit: " + user_input)
        return user_input

    def askQuestion(self, question):
        self.speak(question)
        rand = random.choice([True, False])
        if rand:
            self.response_user = self.listenMicrophone()
        else:
            self.response_user = self.listenConsole()
