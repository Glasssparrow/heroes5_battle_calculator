from math import copysign, floor
from random import random
from simulator.simulator_keywords import *


def calculate_damage(damage, attack, defence, max_damage):
    sign = copysign(1, attack - defence)
    amount_of_damage = (
        damage * (1 + 0.05 * abs(attack - defence)) ** sign
    )
    # По игровой механике урон округляется вниз
    amount_of_damage = floor(amount_of_damage)
    if amount_of_damage > max_damage:
        return max_damage
    else:
        return amount_of_damage


def check_random(chance):
    if not isinstance(chance, (int, float)):
        raise Exception(
            "Не верный тип данных"
        )
    if chance < 0 or chance > 1:
        raise Exception(
            "Не в промежутке 0 < chance < 1"
        )
    if chance > random():
        return True
    else:
        return False


def calculate_base_chance(user, target):
    if user.hp > target.hp:
        chance = 0.25 + 0.03 * user.hp/target.hp
    else:
        chance = 0.25 - 0.03 * target.hp/user.hp
    if chance < 0.05:
        return 0.05
    elif chance > 0.75:
        return 0.75
    else:
        return chance


def check_ghost(target):
    if GHOST not in target.special_attributes:
        return False
    else:
        if check_random(0.5):
            print(f"{target.name} уклоняется!")
            return True
        else:
            print(f"{target.name} не удалось уклониться!")
            return False
