from .common import Effect
from simulator.simulator_keywords import *


class DexterityBuff(Effect):

    def __init__(self):
        super().__init__()
        self.defence = 14
        self.name = "Ловкость (бафф)"

    def reapply(self, new_instance):
        self.defence = new_instance.defence


class DivineStrengthNoSkill(Effect):

    def __init__(self):
        super().__init__()
        self.name = "божественная сила (нет навыка)"
        self.damage = 0.5
        self.time = 3


class DivineStrengthBasics(Effect):

    def __init__(self):
        super().__init__()
        self.name = "божественная сила (основы)"
        self.damage = 0.65
        self.time = 3


class DivineStrengthAdvanced(Effect):

    def __init__(self):
        super().__init__()
        self.name = "божественная сила (сильная)"
        self.damage = 0.8
        self.time = 3


class DivineStrengthExpert(Effect):

    def __init__(self):
        super().__init__()
        self.name = "божественная сила (эксперт)"
        self.damage = 1
        self.time = 3


class Invisibility(Effect):

    def __init__(self):
        super().__init__()
        self.name = "невидимость"
        self.time = 3
        self.special_effects = [INVISIBILITY]
