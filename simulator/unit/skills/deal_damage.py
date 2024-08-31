from .common import Skill
from simulator.simulator_keywords import *
from random import randint
from ..common import calculate_damage
from math import floor


class Kill1Extra(Skill):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Убивает на 1 существо больше"
        self.activation_cases.append(ACTIVATE_BEFORE_STRIKE)

    @staticmethod
    def use(target, damage, kills, battle_map):
        killed_by_skill = target.take_damage(target.health)
        print(f"{target.name} получает {target.health} урона. Погибло "
              f"{killed_by_skill} существ.")


class Deal2DamageToEach(Skill):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "2 урона каждому существу"
        self.activation_cases.append(ACTIVATE_BEFORE_STRIKE)

    @staticmethod
    def use(target, damage, kills, battle_map):
        quantity = target.quantity*2
        killed_by_skill = target.take_damage(target.quantity*2)
        print(f"{target.name} получает {quantity} урона. Погибло "
              f"{killed_by_skill} существ.")


class ThunderStrike(Skill):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Удар бури"
        self.activation_cases.append(ACTIVATE_AFTER_STRIKE)

    def use(self, target, damage, kills, battle_map):
        min_damage = int(
            self.owner.min_damage * self.owner.quantity
        )
        max_damage = int(
            self.owner.max_damage * self.owner.quantity
        )
        damage = calculate_damage(
            damage=randint(min_damage, max_damage),
            attack=self.owner.attack,
            defence=target.defence,
            max_damage=target.hp
        )
        kills = target.take_damage(damage)
        print(f"{self.owner.name} наносит {target.name}. "
              f"{damage} урона при помощи удара бури. "
              f"Погибло {kills} {target.name}. "
              f"Осталось {target.quantity}")


class FireShield20(Skill):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Огненный щит 20"
        self.activation_cases.append(ACTIVATE_AFTER_GET_HIT)

    @staticmethod
    def use(target, damage, kills, battle_map):
        killed_by_skill = target.take_damage(floor(damage*0.2))
        print(f"{target.name} получает {floor(damage*0.2)} урона "
              f"от огненного щита. Погибло "
              f"{killed_by_skill} существ.")


class FireShield40(Skill):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Огненный щит 40"
        self.activation_cases.append(ACTIVATE_AFTER_GET_HIT)

    @staticmethod
    def use(target, damage, kills, battle_map):
        killed_by_skill = target.take_damage(floor(damage*0.4))
        print(f"{target.name} получает {floor(damage*0.4)} урона "
              f"от огненного щита. Погибло "
              f"{killed_by_skill} существ.")
