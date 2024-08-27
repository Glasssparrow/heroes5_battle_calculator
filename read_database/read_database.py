

class DataBase:

    def __init__(self):
        self.the_unit = "the_unit"

    def get_unit(self, unit_name):
        return self.the_unit


def read_data():
    # Данные стоит держать в виде ods таблицы, не xls.
    return DataBase()
