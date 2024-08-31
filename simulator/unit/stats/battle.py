from .common import Stat
from math import floor


class MinDamage(Stat):

    def __set_name__(self, owner, name):
        self.name = "_" + name
        self.stat = "damage"

    def __get__(self, instance, owner):
        min_damage = instance.__dict__["_min_damage"]
        max_damage = instance.__dict__["_max_damage"]
        difference = max_damage - min_damage
        total_buffs_effect = 0
        for buff in instance.__dict__["effects"]:
            total_buffs_effect += buff.__dict__[self.stat]
        if total_buffs_effect > 0:
            result = min_damage + total_buffs_effect * difference
        else:
            result = min_damage
        result = floor(result)
        if result < 0:
            return 0
        elif result > max_damage:
            return max_damage
        else:
            return result


class MaxDamage(MinDamage):

    def __get__(self, instance, owner):
        min_damage = instance.__dict__["_min_damage"]
        max_damage = instance.__dict__["_max_damage"]
        difference = max_damage - min_damage
        total_buffs_effect = 0
        for buff in instance.__dict__["effects"]:
            total_buffs_effect += buff.__dict__[self.stat]
        if total_buffs_effect < 0:
            result = min_damage + (1+total_buffs_effect) * difference
        else:
            result = max_damage
        result = floor(result)
        if result < 0:
            return 0
        elif result < min_damage:
            return min_damage
        else:
            return result

    def __set__(self, instance, value):
        min_damage = instance.__dict__["_min_damage"]
        if value < min_damage:
            instance.__dict__[self.name] = min_damage
        else:
            instance.__dict__[self.name] = value


class Health(Stat):

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]
