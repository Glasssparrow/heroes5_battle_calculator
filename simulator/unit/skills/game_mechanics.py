from .common import Skill
from simulator.simulator_keywords import *


class DispellAfterTakingDamage(Skill):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Снятие дебафов снимаемых уроном (игровая механика)"
        self.activation_cases = [
            ACTIVATE_AFTER_GET_HIT, ACTIVATE_AFTER_GET_SHOT,
        ]

    def use(self, target, damage, kills, battle_map):
        self.owner.dispell_by_case(DISPELL_AFTER_TAKING_DAMAGE)
