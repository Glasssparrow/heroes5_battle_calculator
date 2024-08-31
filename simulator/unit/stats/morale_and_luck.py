from .common import Stat
from math import floor
from ..simulator_keywords import *


class Luck(Stat):

    def __get__(self, instance, owner):
        result = instance.__dict__[self.name]
        for buff in instance.__dict__["effects"]:
            result += buff.__dict__[self.stat]
        result = floor(result)
        if result < -5:
            return -5
        elif result > 5:
            return 5
        else:
            return result


class Morale(Stat):

    def __get__(self, instance, owner):
        result = instance.__dict__[self.name]
        for buff in instance.__dict__["effects"]:
            result += buff.__dict__[self.stat]
            if ZERO_MORALE in buff.special_effects:
                return 0
        result = floor(result)
        if result < -5:
            return -5
        elif result > 5:
            return 5
        else:
            return result
