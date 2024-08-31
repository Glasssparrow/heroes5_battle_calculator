from .common import Effect
from simulator.simulator_keywords import *


class LowMoraleEffect(Effect):

    def __init__(self):
        super().__init__()
        self.name = "Нерешительность"
        self.initiative_mark = INITIATIVE_MORALE
        self.special_effects.append(BLOCK_ACTION)
        self.dispell_conditions = [DISPELL_CASE_INITIATIVE]


class HighMoraleEffect(Effect):

    def __init__(self):
        super().__init__()
        self.name = "Воодушевление"
        self.initiative_mark = INITIATIVE_MORALE
        self.dispell_conditions = [DISPELL_CASE_INITIATIVE]


class AlwaysZeroMorale(Effect):

    def __init__(self):
        super().__init__()
        self.name = "undead"
        self.special_effects = [ZERO_MORALE]
