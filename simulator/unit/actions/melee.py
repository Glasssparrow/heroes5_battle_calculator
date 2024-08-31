from keywords import *
from random import randint
from ..common import (
    calculate_damage, calculate_base_chance,
    check_ghost
)
from .common import Action, is_slowed


class Melee(Action):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Атака в ближнем бою"
        self.keyword = MELEE_ATTACK

    def act(self, target, battle_map):
        if not self.can_unit_act(target, battle_map):
            return
        if self.is_melee_attack_possible(target, battle_map):
            self.strike(target, battle_map)
            target.react(MELEE_COUNTER, self.owner, battle_map)

    def strike(self, target, battle_map):
        if check_ghost(target):
            return 0
        damage_modifier = self.calculate_damage_modifier(target)
        min_damage = int(
            self.owner.min_damage * self.owner.quantity * damage_modifier
        )
        max_damage = int(
            self.owner.max_damage * self.owner.quantity * damage_modifier
        )
        damage = calculate_damage(
            damage=randint(min_damage, max_damage),
            attack=self.owner.attack,
            defence=target.defence,
            max_damage=target.hp
        )
        self.before_action(target, battle_map)
        kills = target.take_damage(damage)
        print(f"{self.owner.name} атакует {target.name}. "
              f"Наносит {damage} урона. "
              f"Погибло {kills} {target.name}. "
              f"Осталось {target.quantity}")
        self.after_action(target, damage, kills, battle_map)
        return kills

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

    def calculate_damage_modifier(self, target):
        shield_wall = shield_wall = self.calculate_shield_wall_modifier(
            self.owner, target)
        return shield_wall * self.luck_modifier()

    @staticmethod
    def is_melee_attack_possible(target, battle_map):
        for effect in target.effects:
            for special_effect in effect.special_effects:
                if special_effect == INVISIBILITY:
                    print(f"Атака невозможна т.к. {target.name} "
                          f"невидим")
                    return False
        return True

    def before_action(self, target, battle_map):
        self.owner.use_skills(
            skill_type=ACTIVATE_BEFORE_STRIKE,
            target=target, battle_map=battle_map
        )
        target.use_skills(
            skill_type=ACTIVATE_BEFORE_GET_HIT,
            target=self.owner, battle_map=battle_map
        )

    def after_action(self, target, damage, kills, battle_map):
        self.owner.use_skills(
            skill_type=ACTIVATE_AFTER_STRIKE, target=target,
            damage=damage, kills=kills, battle_map=battle_map
        )
        target.use_skills(
            skill_type=ACTIVATE_AFTER_GET_HIT, target=self.owner,
            damage=damage, kills=kills, battle_map=battle_map,
        )


class ChivalryCharge(Melee):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Рыцарский удар"

    def calculate_damage_modifier(self, target):
        shield_wall = self.calculate_shield_wall_modifier(
            self.owner, target)
        damage_modifier = 1 + 0.05 * self.owner.tiles_moved
        damage_modifier = (
            damage_modifier * self.luck_modifier() * shield_wall
        )
        return damage_modifier


class DoubleAttackIfKill(Melee):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Колун"

    def act(self, target, battle_map):
        if not self.can_unit_act(target, battle_map):
            return
        if self.is_melee_attack_possible(target, battle_map):
            kills = self.strike(target, battle_map)
            target.react(MELEE_COUNTER, self.owner, battle_map)
            if kills > 0:
                self.strike(target, battle_map)
                target.react(MELEE_COUNTER, self.owner, battle_map)


class DoubleAttack(Melee):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Двойной удар"

    def act(self, target, battle_map):
        if not self.can_unit_act(target, battle_map):
            return
        if self.is_melee_attack_possible(target, battle_map):
            self.strike(target, battle_map)
            target.react(MELEE_COUNTER, self.owner, battle_map)
            self.strike(target, battle_map)
            target.react(MELEE_COUNTER, self.owner, battle_map)


class MeleeNoCounter(Melee):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Безответный удар"

    def act(self, target, battle_map):
        if not self.can_unit_act(target, battle_map):
            return
        if self.is_melee_attack_possible(target, battle_map):
            self.strike(target, battle_map)


class WeakMelee(Melee):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Слабый удар"

    def calculate_damage_modifier(self, target):
        shield_wall = self.calculate_shield_wall_modifier(
            self.owner, target)
        damage_modifier = (
            0.5 * self.luck_modifier() * shield_wall
        )
        return damage_modifier


class LizardCharge(Melee):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Удар с разбега (ящеры)"

    def strike(self, target, battle_map):
        if check_ghost(target):
            return 0
        damage_modifier = self.calculate_damage_modifier(target)
        min_damage = int(
            self.owner.min_damage * self.owner.quantity * damage_modifier
        )
        max_damage = int(
            self.owner.max_damage * self.owner.quantity * damage_modifier
        )
        enemy_defence = (
            self.calculate_enemy_defence_modifier() * target.defence
        )
        print(f"Часть защиты {target.name} проигнорирована. "
              f"Расчетная защита {enemy_defence}")
        damage = calculate_damage(
            damage=randint(min_damage, max_damage),
            attack=self.owner.attack,
            defence=enemy_defence,
            max_damage=target.hp
        )
        self.before_action(target, battle_map)
        kills = target.take_damage(damage)
        print(f"{self.owner.name} атакует {target.name}. "
              f"Наносит {damage} урона. "
              f"Погибло {kills} {target.name}. "
              f"Осталось {target.quantity}")
        self.after_action(target, damage, kills, battle_map)
        return kills

    def calculate_enemy_defence_modifier(self):
        modifier = 1 - 0.2 * self.owner.tiles_moved
        if modifier < 0:
            return 0
        else:
            return modifier


class Assault(Melee):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Штурм"
        self.keyword = MELEE_ATTACK

    def act(self, target, battle_map):
        if not self.can_unit_act(target, battle_map):
            return
        if self.is_melee_attack_possible(target, battle_map):
            self.strike(target, battle_map)
            target.react(MELEE_COUNTER, self.owner, battle_map)
            if self.is_2_attack_worked(target):
                self.strike(target, battle_map)
                target.react(MELEE_COUNTER, self.owner, battle_map)

    def is_2_attack_worked(self, target):
        base_chance = calculate_base_chance(self.owner, target)
        return 1-(1-base_chance)


class MeleeNoCounterIfSlowed(Melee):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Безответный удар если враг замедлен"

    def act(self, target, battle_map):
        if not self.can_unit_act(target, battle_map):
            return
        if self.is_melee_attack_possible(target, battle_map):
            self.strike(target, battle_map)
            if not is_slowed(target):
                target.react(MELEE_COUNTER, self.owner, battle_map)
