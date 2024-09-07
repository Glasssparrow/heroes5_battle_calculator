from simulator import *


class DataBase:

    def __init__(self):
        self.for_unit1 = {
            "name": "Пугало",
            "attack": 1, "defence": 1, "min_damage": 1, "max_damage": 1,
            "health": 50, "initiative": 8, "speed": 4,
            "mana": 0, "ammo": 0,
        }
        self.for_unit2 = {
            "name": "Манекен",
            "attack": 1, "defence": 1, "min_damage": 1, "max_damage": 1,
            "health": 50, "initiative": 8, "speed": 4,
            "mana": 0, "ammo": 0,
        }

    def get_unit(self, unit_name):
        if unit_name == "Манекен":
            the_unit = Unit(**self.for_unit1)
        else:
            the_unit = Unit(**self.for_unit2)
        the_unit.add_action(Melee)
        return the_unit


def read_data():
    # Данные стоит держать в виде ods таблицы, не xls.
    return DataBase()
