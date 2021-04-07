from bot import *
from board import *

class Gameplay:

    def __init__(self):
        self.board = Board(3)
        self.bot = Bot('fr', self.board)

    def loop(self):
        found_victim = False
        while True:
            self.bot.move()
            current_room = self.bot.current_room
            self.bot.memorize(current_room.get_character().get_name() + ' se trouve dans le ' + current_room.get_name())
            self.bot.memorize('Le ' + current_room.get_weapon().get_name() + ' se trouve dans le ' + current_room.get_name())

            # We already know who the victim is, but the bot does not
            if current_room.get_is_crime_room() and not found_victim:
                self.bot.memorize('Alex est mort')
                self.bot.memorize('Alex se trouve dans le ' + current_room.get_name())
                self.bot.memorize('Alex a ' + self.board.get_crime_injury())
                response = self.bot.askQuestion('À quelle heure est mort Alex?')
                self.bot.memorize(response)

                for character in self.board.get_characters_string():
                    if character is 'Alex':
                        continue
                    self.bot.memorize(character + ' est vivant')
                found_victim = True

            if found_victim:
                response = self.bot.askQuestion('Où se trouvait ' + current_room.get_character().get_name() +
                                                ' à ' + str(self.bot.moteur_inference.get_crime_hour() + 1) + 'h?')
                self.bot.memorize(response)

            if self.bot.try_solve_crime():
                hour, room, suspect, weapon, innocents, victim = self.bot.moteur_inference.get_crime_info()
                self.bot.speak(suspect + ' a tué ' + victim + ' avec un ' + weapon + ' dans le ' + room + ' à ' + hour + ' heure.')
                break

