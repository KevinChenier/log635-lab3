import os.path

class FileReader:
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        self.counter = 0
        self.args = []

    def getfiletext(self, file):
        my_file = os.path.join(self.THIS_FOLDER, file)
        text_file = open(my_file)
        return text_file.read()
