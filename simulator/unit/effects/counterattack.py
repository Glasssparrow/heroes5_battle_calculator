from .common import Effect
from ..simulator_keywords import *


class BattleFrenzy(Effect):

    def __init__(self):
        super().__init__()
        self.name = "battle_frenzy"
        self.modifiers[BATTLE_FRENZY_MODIFIER] = 1.5
        self.dispell_conditions.append(DISPELL_AT_TURN_START)

    def reapply(self, new_instance):
        self.modifiers[BATTLE_FRENZY_MODIFIER] = (
            self.modifiers[BATTLE_FRENZY_MODIFIER] * 1.5
        )


class BlockCounter(Effect):

    def __init__(self):
        super().__init__()
        self.name = "block_counter"
        self.special_effects.append(BLOCK_COUNTER)
        self.dispell_conditions.append(DISPELL_AT_TURN_START)
