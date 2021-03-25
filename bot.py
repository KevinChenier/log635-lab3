from Ressources.SyntheseVocaleSimple.tts import *
from fileReader import *
import speech_recognition as sr
sr.__version__

class Bot:

    voice = Tts('en')
    voice_recognizer = sr.Recognizer()
    micro = sr.Microphone()

    file_reader = FileReader()

    text_memorized = ''
    questions = 'How are you?', 'Where are you?', 'Who are you?'

    def __init__(self, language):
        self.voice = Tts(language)

    def readFileText(self, fileName):
        return self.file_reader.getfiletext(fileName)

    def speak(self, textToSay):
        print(textToSay)
        self.voice.playaudio(textToSay)

    def memorize(self, text):
        self.text_memorized = text
        print('Text memorized:', text)

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
        print("Listening...")
        response = self.recognize_speech_from_mic()

        transcription = response["transcription"]
        # show the user the transcription
        self.speak("You said: {}".format(transcription))
        return transcription

    def listenConsole(self):
        print("Enter your text: ")
        user_input = input()
        self.speak("You wrote: " + user_input)
        return user_input

    def askQuestion(self, question):
        self.voice.playaudio(question)
        print(question)