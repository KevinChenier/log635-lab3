class Weapon:

    def __init__(self, name, location, location_during_crime, is_crime_weapon):
        self.name = name
        self.location = location
        self.location_during_crime = location_during_crime
        self.is_crime_weapon = is_crime_weapon

    def get_name(self):
        return self.name

    def get_location(self):
        return self.location

    def get_is_crime_weapon(self):
        return self.is_crime_weapon