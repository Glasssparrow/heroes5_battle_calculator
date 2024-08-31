from ..common import check_random


class Reaction:

    def __init__(self, owner):
        self.name = "default"
        self.owner = owner
        self.keyword = "no keyword"

    def luck_modifier(self):
        luck = self.owner.luck
        if luck == 0:
            return 1
        elif luck < 0:
            if check_random(luck * -0.1):
                return 0.5
            else:
                return 1
        else:
            if check_random(luck * 0.1):
                return 2
            else:
                return 1

    def calculate_damage_modifier(self):
        return self.luck_modifier()
