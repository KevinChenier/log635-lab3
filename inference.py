##############
#1.1 paquets #
##############

#from Ressources.SystemeDeRaisonnement.aima import *
from aima.logic import *
import nltk

#Moteur de déduction basé sur la doc AIMA fourni 
class inference:
    
    # Permet d'inferer qui est le meurtrier, quand, comment, où il a tué.
    def __init__(self, weapons, rooms, persons):

        self.weapons = weapons
        self.rooms = rooms
        self.persons = persons
        
        # Liste de clauses (faits) qui seront stockées dans la base de connaissance.
        self.clauses = []        
        
        self.base_clauses()
        self.initialize_KB()
        self.inference_rules()
        
        # Base de connaissances (First-order logic - FOL)
        self.crime_kb = FolKB(self.clauses)

    # Déclaration dans la logique du premier ordre
    def base_clauses(self):
        # Le paramètre est une arme
        self.arme_clause = 'Arme({})'
        
        # Le paramètre est une pièce
        self.piece_clause = 'Piece({})'
        
        # Le paramètre est une persone
        self.personne_clause = 'Personne({})'

        # paramètre 1 : arme; paramètre 2 : pièce
        # p.ex.: Le couteau se trouve dans la cuisine
        self.weapon_room_clause = 'Arme_Piece({},{})'

        # paramètre 1 : personne; paramètre 2 : pièce; paramètre 3 : heure
        # p.ex.: Mustart était dans la cuisine à 11h00
        self.person_room_hour_clause = 'Personne_Piece_Heure({}, {}, {})'

        # paramètre 1 : personne; paramètre 2 : piece
        # p.ex.: Mustard se trouve dans la cuisine
        self.person_room_clause = 'Personne_Piece({}, {})'

        # paramète 1 : personne
        # p. ex.: Mustard est mort
        self.dead_clause = 'EstMort({})'
        
        # paramète 1 : personne
        # p. ex.: Mustard est vivant
        self.alive_clause = 'EstVivant({})'

        # paramètre 1 : personne
        # p. ex.: Mustard est la victime
        self.victim_clause = 'Victime({})'

        # paramètre 1 : personne
        # p. ex.: Mustard a des marques au cou
        self.body_mark_clause = 'MarqueCou({})'

        # paramètre 1 : piece; paramètre 2 : piece
        self.room_different_clause = 'PieceDifferente({},{})'

        # paramètre 1 : piece; paramètre 2 : piece
        self.weapon_different_clause = 'ArmeDifferente({},{})'

        # paramètre 1 : heure
        self.crime_hour_clause = 'HeureCrime({})'

        # paramètre 1 : heure
        self.crime_hour_plus_one_clause = 'UneHeureApresCrime({})'

    def initialize_KB(self):
        # Clause pour differencier les pièces
        for i in range(len(self.rooms)):
            for j in range(len(self.rooms)):
                if i != j:
                    # Le bureau est different de la cuisine = PieceDifferente(Bureau, Cuisine)
                    self.clauses.append(expr(self.room_different_clause.format(self.rooms[i], self.rooms[j])))

        # Clause pour differencier les armes
        for i in range(len(self.weapons)):
            for j in range(len(self.weapons)):
                if i != j:
                    # Le couteau est different de la corde = ArmeDifferente(Couteau, Corde)
                    self.clauses.append(expr(self.weapon_different_clause.format(self.weapons[i], self.weapons[j])))

        # Initialiser KB sur Armes, Pieces, Personnes
        for weapon in self.weapons:
            # Le couteau est une arme = Arme(Couteau)
            self.clauses.append(expr(self.arme_clause.format(weapon)))

        for room in self.rooms:
            # La cuisine est une pièce = Piece(Cuisine)
            self.clauses.append(expr(self.piece_clause.format(room)))

        for person in self.persons:
            # Mustar est une personne = Personne(Mustard)
            self.clauses.append(expr(self.personne_clause.format(person)))
    
    # Expressions dans la logique du premier ordre permettant de déduire les caractéristiques du meurtre
    def inference_rules(self):
        # Determine la piece du crime
        self.clauses.append(expr('EstMort(x) & Personne_Piece(x, y) ==> PieceCrime(y)'))

        # Determiner l'arme du crime
        self.clauses.append(expr('PieceCrime(x) & Arme(y) & Piece_Arme(y, x) ==> ArmeCrime(y)'))
        self.clauses.append(expr("EstMort(x) & MarqueCou(x) ==> ArmeCrime(Corde)"))

        # Si la personne est morte alors elle est la victime et ce n'est pas un suicide
        self.clauses.append(expr('EstMort(x) ==> Victime(x)'))

        # Si la personne est morte alors elle est innocente et ce n'est pas un suicide
        self.clauses.append(expr('EstMort(x) ==> Innocent(x)'))

        # Si la personne est vivante et était dans une pièce
        # qui ne contient pas l'arme du crime, alors elle est innocente
        self.clauses.append(expr(
            'EstVivant(p) & UneHeureApresCrime(h1) & Personne_Piece_Heure(p,r2,h1) & PieceCrime(r1)'
            ' & PieceDifferente(r1,r2) & ArmeCrime(a1) & Arme_Piece(a2,r2) & ArmeDifferente(a1,a2) ==> Innocent(p)'))

        # Si la personne se trouvait dans une piece qui contient l'arme
        # qui a tué la victime une heure après le meurtre alors elle est suspecte
        self.clauses.append(expr(
            'EstVivant(p) & UneHeureApresCrime(h1) & Personne_Piece_Heure(p,r2,h1) & PieceCrime(r1)'
            ' & PieceDifferente(r1,r2) & ArmeCrime(a) & Arme_Piece(a,r2) ==> Suspect(p)'))

    # Ajouter des clauses, c'est-à-dire des faits, à la base de connaissances
    def add_clause(self, clause_string):
        self.crime_kb.tell(expr(clause_string))

    # Demander à la base de connaissances qui est la victime
    def get_victim(self):
        result = self.crime_kb.ask(expr('Victime(x)'))
        if not result:
            return False
        else:
            return result[x]
        
    # Demander à la base de connaissances la pièce du meurtre
    def get_crime_room(self):
        result = self.crime_kb.ask(expr('PieceCrime(x)'))
        if not result:
            return False
        else:
            return result[x]

    # Demander à la base de connaissances l'arme du meurtrier
    def get_crime_weapon(self):
        result = self.crime_kb.ask(expr('ArmeCrime(x)'))
        if not result:
            return result
        else:
            return result[x]

    # Demander à la base de connaissances l'heure du meurtre
    def get_crime_hour(self):
        result = self.crime_kb.ask(expr('HeureCrime(x)'))
        if not result:
            return result
        else:
            return result[x]

    def get_crime_hour_plus_one(self):
        result = self.crime_kb.ask(expr('UneHeureApresCrime(x)'))
        if not result:
            return result
        else:
            return result[x]
    
    # Demander à la base de connaissances le suspect
    def get_suspect(self):
        result = self.crime_kb.ask(expr('Suspect(x)'))
        if not result:
            return result
        else:
            return result[x]

    # Cette fonction retourne le format d'une expression logique de premier ordre
    def results_as_string(self, results):
        res = ''
        for result in results:
            # synrep = syntactic representation
            # semrep = semantic representation
            for (synrep, semrep) in result:            
                res += str(semrep)
        return res

    # Cette fonction transforme une phrase en français dans une expression logique du premier ordre
    def to_fol(self, fact, grammar):
        sent = self.results_as_string(nltk.interpret_sents(fact, grammar))
        print(sent)
        return sent

    def get_last_clause(self):
        if self.clauses:
            return self.clauses[-1]

'''
    ### MAIN? ###    
    #Creation d'une instance du moteur d'inference
    agent = inference()
    # Faits
    facts = [['Scarlet est morte'],
            ['Mustard est vivant'],
            ['Peacock est vivant'],
            ['Plum est vivant'],
            ['White est vivant']]

    # Les fait sont ajoutés à la base de connaissances
    agent.add_clause(to_fol(facts[0], 'grammaires/personne_morte.fcfg'))
    facts.pop(0)

    for fact in facts:    
        agent.add_clause(to_fol(fact, 'grammaires/personne_vivant.fcfg'))



    # Dans le salon
    # Voit qu'il y a un fusil et Plum dans le salon
    fact = ['Le fusil est dans le salon']
    agent.add_clause(to_fol(fact, 'grammaires/arme_piece.fcfg'))

    fact = ['Plum est dans le salon']
    agent.add_clause(to_fol(fact, 'grammaires/personne_piece.fcfg'))

    # Demande à Plum dans quelle pièce il était une heure après le meurtre -> Rep : Plum dans le Salon à 15h
    fact = ['Plum était dans le salon à ' + str(uneHeureApres) + 'h']
    agent.add_clause(to_fol(fact, 'grammaires/personne_piece_heure.fcfg'))



    # Dans la cuisine
    # Voit qu'il y a un couteau, White et Mustard dans la cuisine
    fact = ['Le couteau est dans la cuisine']
    agent.add_clause(to_fol(fact, 'grammaires/arme_piece.fcfg'))

    fact = ['White est dans la cuisine']
    agent.add_clause(to_fol(fact, 'grammaires/personne_piece.fcfg'))

    fact = ['Mustard est dans la cuisine']
    agent.add_clause(to_fol(fact, 'grammaires/personne_piece.fcfg'))

    # Demande à White dans quelle pièce il était une heure après le meurtre -> Rep : White dans la Cuisine à 15h
    fact = ['White était dans la cuisine à ' + str(uneHeureApres) + 'h']
    agent.add_clause(to_fol(fact, 'grammaires/personne_piece_heure.fcfg'))

    # Demande à Mustard dans quelle pièce il était une heure après le meurtre -> Rep : Mustard dans le Garage à 15h
    fact = ['Mustard était dans le garage à ' + str(uneHeureApres) + 'h']
    agent.add_clause(to_fol(fact, 'grammaires/personne_piece_heure.fcfg'))


    # Dans le garage
    # On se rend compte qu'il y a une corde dans le garage
    fact = ['La corde est dans le garage']
    agent.add_clause(to_fol(fact, 'grammaires/arme_piece.fcfg'))


    # Conclusions
    print("Pièce du crime : ", agent.get_crime_room())
    print("Arme du crime : ", agent.get_crime_weapon())
    print("Personne victime : ", agent.get_victim())
    print("Heure du crime : ", agent.get_crime_hour())
    print("Meurtrier : ", agent.get_suspect())
    print("Personnes innocentes : ", agent.get_innocent()) 
'''