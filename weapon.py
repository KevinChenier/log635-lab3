class Weapon:

    def __init__(self, name, location, location_one_hour_after_crime, is_crime_weapon):
        self.name = name
        self.location = location
        self.location_one_hour_after_crime = location_one_hour_after_crime
        self.is_crime_weapon = is_crime_weapon

    def get_name(self):
        return self.name