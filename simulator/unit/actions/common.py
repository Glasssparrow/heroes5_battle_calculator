from ..common import check_random
from ...simulator_keywords import *
from ..effects import SlowNoSkill, SlowBasics, SlowAdvanced, SlowExpert


class Action:

    def __init__(self, owner):
        self.name = "default"
        self.owner = owner
        self.after_move = True
        self.blocked_in_melee = False
        self.require_mana = 0
        self.require_ammo = 0
        # Данные для decisionmaker.
        self.threat = 1
        self.range = None
        self.type_of_action = JUST_MOVEMENT

    def act(self, target, battle_map):
        pass

    def move_and_act(self, target, battle_map, new_position):
        if not self.can_unit_act(target, battle_map):
            return
        x, y = new_position[0], new_position[1]
        battle_map.move_unit(self, x, y)
        self.act(target, battle_map)

    def can_unit_act(self, target, battle_map):
        if not self.owner.hp > 0:
            print(f"{self.owner.name} не может действовать т.к. мертв.")
            return False
        if not target.hp > 0:
            print(f"{self.owner.name} не может действовать т.к. "
                  f"цель мертва.")
            return False
        for effect in self.owner.effects:
            if BLOCK_ACTION in effect.special_effects:
                print(f"{self.owner.name} ожидает в нерешительности.")
                return False
        return True

    def can_be_used(self):
        # Проверяет достаточно ли маны или боеприпасов.
        if self.require_ammo > self.owner.ammo:
            return False
        if self.require_mana > self.owner.mana:
            return False
        return True

    def luck_modifier(self):
        luck = self.owner.luck
        if luck == 0:
            return 1
        elif luck < 0:
            if check_random(luck * -0.1):
                return 0.5
            else:
                return 1
        else:
            if check_random(luck * 0.1):
                return 2
            else:
                return 1

    def calculate_damage_modifier(self, target):
        return self.luck_modifier()

    @staticmethod
    def calculate_shield_wall_modifier(owner, target):
        shield_wall = 1
        for special_attribute in target.special_attributes:
            if special_attribute == WALL_OF_SHIELDS:
                if owner.tiles_moved > 9:
                    shield_wall = 0.1
                else:
                    shield_wall = 1 - 0.1 * owner.tiles_moved
        return round(shield_wall, 1)


def is_slowed(unit):
    for effect in unit.effects:
        if isinstance(effect, (
                SlowNoSkill, SlowBasics, SlowAdvanced, SlowExpert
        )):
            return True
    return False
