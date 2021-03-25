from Ressources.SyntheseVocaleSimple.tts import *
from fileReader import *
import speech_recognition as sr
import random
sr.__version__

class Bot:

    voice = Tts('fr')
    voice_recognizer = sr.Recognizer()
    micro = sr.Microphone()

    file_reader = FileReader()

    info_to_analyze = ''
    questions = "Ou suis-je?", \
                "Qu'est-ce que c'est?"
    response = ''

    def __init__(self, language):
        self.voice = Tts(language)

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
            response["transcription"] = self.voice_recognizer.recognize_google(audio)
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
            self.response = self.listenConsole()
        else:
            self.response = self.listenMicrophone()
