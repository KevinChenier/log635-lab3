class Character:

    def __init__(self, name, location, location_one_hour_after_crime, is_killer):
        self.name = name
        self.location = location
        self.location_one_hour_after_crime = location_one_hour_after_crime
        self.is_killer = is_killer

    def get_name(self):
        return self.name

    def get_location_one_hour_after_crime(self):
        return self.location_one_hour_after_crime
