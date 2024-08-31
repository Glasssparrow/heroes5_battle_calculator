

class Initiative:

    def __init__(self, units: list):
        self.units = units
        self.active_unit_index = -1

    def get_active_unit(self):
        self.active_unit_index += 1
        if self.active_unit_index < len(self.units):
            pass
        else:
            self.active_unit_index = 0
        return self.units[self.active_unit_index]
