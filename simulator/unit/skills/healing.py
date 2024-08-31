from .common import Skill
from simulator.simulator_keywords import *
from math import floor


class Vampire(Skill):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Вампиризм"
        self.activation_cases.append(ACTIVATE_AFTER_STRIKE)

    def use(self, target, damage, kills, battle_map):
        amount_of_healing = floor(damage/2)
        if target.check_immunity(VAMPIRISM_IMMUNE):
            print(f"Вампиризм не сработал на {target.name}")
        else:
            revived = self.owner.take_healing(amount_of_healing)
            print(f"{self.owner.name} исцеляется на {amount_of_healing} "
                  f"ударив {target.name}. "
                  f"Возродилось {int(revived)} существ.")
