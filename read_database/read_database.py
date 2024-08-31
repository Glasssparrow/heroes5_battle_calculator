from simulator.unit.unit import Unit


class DataBase:

    def __init__(self):
        self.for_unit1 = {
            "name":"Пугало",
            "attack":1, "defence":1, "min_damage":1, "max_damage":1,
            "health":1000, "initiative":8, "speed":4,
            "mana":0, "ammo":0,
        }

    def get_unit(self, unit_name):
        return Unit(**self.for_unit1)


def read_data():
    # Данные стоит держать в виде ods таблицы, не xls.
    return DataBase()
