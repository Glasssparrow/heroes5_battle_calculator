from .common import Effect
from simulator.simulator_keywords import *


class Bash(Effect):

    def __init__(self):
        super().__init__()
        self.name = "bash"
        self.special_effects.append(BASH)
        self.dispell_conditions.append(DISPELL_CASE_INITIATIVE)
