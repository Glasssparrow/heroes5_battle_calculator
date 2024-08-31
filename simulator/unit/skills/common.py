from ..common import calculate_base_chance


class Skill:

    def __init__(self, owner):
        self.owner = owner
        self.name = "default"
        self.activation_cases = []
