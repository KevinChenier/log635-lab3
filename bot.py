from random import random

import keyboard
from Ressources.SyntheseVocaleSimple.tts import *
from fileReader import *
import speech_recognition as sr
from inference import *
import random

sr.__version__

class Bot:
    voice_recognizer = sr.Recognizer()
    micro = sr.Microphone()
    file_reader = FileReader()

    questions = "Ou suis-je?", \
                "Qu'est-ce que c'est?"


    def __init__(self, language, board):
        self.voice = Tts(language)
        self.board = board
        self.current_room = board.get_rooms()[0]
        self.moteur_inference = inference(board.get_weapons_string(),
                                          board.get_rooms_string(),
                                          board.get_characters_string())

    def readFileText(self, fileName):
        return self.file_reader.getfiletext(fileName)

    def speak(self, textToSay):
        print(textToSay)
        self.voice.playaudio(textToSay)

    def memorize(self, text):
        grammar = self.interpret_text(text)
        self.speak(text)
        self.moteur_inference.add_clause(self.moteur_inference.to_fol([text], grammar))

    def interpret_text(self, text):
        # Heure information
        if any(char.isdigit() for char in text) \
                and any(sub in text for sub in ['se trouvait', 'était dans']) \
                and any(room in text for room in self.board.get_rooms_string()) \
                and any(character in text for character in self.board.get_characters_string()):
            return 'grammaires/personne_piece_heure.fcfg'
        elif any(char.isdigit() for char in text) \
                and any(sub in text for sub in ['mort', 'morte']) \
                and any(character in text for character in self.board.get_characters_string()):
            return 'grammaires/personne_mort_heure.fcfg'

        # Présence d'un objet ou personne dans une piece
        elif any(sub in text for sub in ['trouve', 'est', 'dans']) \
                and any(weapon in text for weapon in self.board.get_weapons_string()) \
                and any(room in text for room in self.board.get_rooms_string()):
            return 'grammaires/arme_piece.fcfg'
        elif any(sub in text for sub in ['trouve', 'est', 'dans']) \
                and any(character in text for character in self.board.get_characters_string()) \
                and any(room in text for room in self.board.get_rooms_string()):
            return 'grammaires/personne_piece.fcfg'

        # Mort ou vivant
        elif any(sub in text for sub in ['est mort', 'est morte'])\
                and any(character in text for character in self.board.get_characters_string()):
            return 'grammaires/personne_mort.fcfg'
        elif any(sub in text for sub in ['est vivant', 'est vivante'])\
                and any(character in text for character in self.board.get_characters_string()):
            return 'grammaires/personne_vivant.fcfg'

        # Blessure
        elif 'plaie' in text\
                and any(character in text for character in self.board.get_characters_string()):
            return 'grammaires/personne_plaie.fcfg'
        elif 'peau' in text\
                and any(character in text for character in self.board.get_characters_string()):
            return 'grammaires/personne_peau.fcfg'
        elif 'trou' in text\
                and any(character in text for character in self.board.get_characters_string()):
            return 'grammaires/personne_trou.fcfg'
        elif any(sub in text for sub in ['marque ', 'marques'])\
                and any(character in text for character in self.board.get_characters_string()):
            return 'grammaires/personne_marque.fcfg'
        elif any(sub in text for sub in ['crâne', 'crane'])\
                and any(character in text for character in self.board.get_characters_string()):
            return 'grammaires/personne_crane.fcfg'

        return "Could not interpret text"

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
        self.speak("J'ai compris: {}".format(transcription) + ", est-ce correcte?")

        if self.confirm():
            self.speak("Confirmé")
            return transcription
        else:
            self.speak("Recommençons,")
            self.listenMicrophone()

    def listenConsole(self):
        print("Entrez votre texte: ")
        user_input = input()
        self.speak("Vous avez écrit: " + user_input + ", est-ce correcte?")

        if self.confirm():
            self.speak("Confirmé")
            return user_input
        else:
            self.speak("Recommençons,")
            self.listenConsole()



    def listenFile(self):
        print("Appuyer sur Enter pour lire le fichier texte")
        while True:

            if(keyboard.is_pressed('Enter')):
                text = self.readFileText('key_log.txt')
                self.speak("Il est écrit dans le fichier: " + text + ", est-ce correcte?")
                if self.confirm():
                    self.speak("Confirmé")
                    return text
                else:
                    self.speak("Réécrivez dans le fichier texte et appuyez Enter")
                    continue

    def move(self):
        print("Appuyez sur [↑] [↓] [←] [→] pour vous déplacer")
        while True:  # making a loop

            if keyboard.is_pressed('up'):
                self.current_room = self.board.get_rooms()[0]
                break

            if keyboard.is_pressed('down'):
                self.current_room = self.board.get_rooms()[-1]
                break

            if keyboard.is_pressed('left'):
                i = self.board.get_rooms().index(self.current_room)
                i = - 1 if i == 0 else i - 1
                self.current_room = self.board.get_rooms()[i]
                break

            if keyboard.is_pressed('right'):
                i = self.board.get_rooms().index(self.current_room)
                i = 0 if i == len(self.board.get_rooms()) - 1 else i + 1
                self.current_room = self.board.get_rooms()[i]
                break
        self.speak("Je suis présentement dans le " + self.current_room.get_name())

    def confirm(self):
        print("Confirmer par [1] Oui ou [2] Non")
        while True:  # making a loop

            if keyboard.is_pressed('1'):
                return True;

            if keyboard.is_pressed('2'):
                # print('You Pressed ↓ Key!')
                return False;

    def askQuestion(self, question):
        self.speak(question)
        channel = random.choice([1, 2, 3])

        if channel is 1:
            return self.listenMicrophone()
        elif channel is 2:
            return self.listenConsole()
        elif channel is 3:
            return self.listenFile()

    def try_solve_crime(self):
        hour, room, suspect, weapon, innocents, victim = self.moteur_inference.get_crime_info()

        if hour and room and suspect and weapon and innocents and victim:
            return True
        else:
            return False

