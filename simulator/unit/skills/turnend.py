from .common import Skill
from ..common import check_random
from ..effects import *
from ..simulator_keywords import *
from random import randint


class HighMorale(Skill):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "+Мораль"
        self.activation_cases.append(ACTIVATE_AT_TURN_END)

    def use(self):
        morale = self.owner.morale
        if morale > 0 and check_random(morale * 0.1):
            self.owner.apply_effect(HighMoraleEffect())


class LowMorale(Skill):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "-Мораль"
        self.activation_cases.append(ACTIVATE_AT_TURN_START)

    def use(self):
        morale = self.owner.morale
        if morale < 0 and check_random(morale * -0.1):
            self.owner.apply_effect(LowMoraleEffect())


class Dexterity(Skill):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Ловкость"
        self.activation_cases.append(ACTIVATE_AT_TURN_END)

    def use(self):
        effect = DexterityBuff()
        effect.defence = self.owner.tiles_moved * 2
        self.owner.apply_effect(effect)


class Regeneration(Skill):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Регенерация"
        self.activation_cases.append(ACTIVATE_AT_TURN_START)

    def use(self):
        amount_of_healing = randint(30, 50)
        self.owner.take_healing(amount_of_healing)
