from random import randint
from ..common import calculate_damage, check_random, check_ghost
from .common import Reaction
from ..effects.counterattack import *
from keywords import *
from ..requirements import run_away


class MeleeCounter(Reaction):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Контратака в ближнем бою"
        self.owner = owner
        self.keyword = MELEE_COUNTER

    def react(self, target, battle_map):
        if not self.can_unit_react(target, battle_map):
            return
        if self.failed_counter():
            return
        self.strike(target, battle_map)

    def strike(self, target, battle_map):
        if check_ghost(target):
            return
        damage_modifier = self.calculate_damage_modifier()
        min_damage = int(
            self.owner.min_damage * self.owner.quantity *
            damage_modifier
        )
        max_damage = int(
            self.owner.max_damage * self.owner.quantity *
            damage_modifier
        )
        damage = calculate_damage(
            damage=randint(min_damage, max_damage),
            attack=self.owner.attack,
            defence=target.defence,
            max_damage=target.hp
        )
        self.before_reaction(target, battle_map)
        kills = target.take_damage(damage)
        self.after_reaction(target, damage, kills, battle_map)
        print(f"{self.owner.name} контратакует {target.name}. "
              f"Наносит {damage} урона. "
              f"Погибло {kills} {target.name}. "
              f"Осталось {target.quantity}")

    def can_unit_react(self, target, battle_map):
        if not self.owner.hp > 0:
            print(f"{self.owner.name} не может реагировать т.к. мертв")
            return False
        if target.hp == 0:
            print(f"{self.owner.name} не может действовать т.к. "
                  f"цель мертва.")
            return False
        for effect in self.owner.effects:
            if BLOCK_COUNTER in effect.special_effects:
                print(f"{self.owner.name} не может контратаковать "
                      f"т.к. эффект {effect.name} блокирует эту "
                      f"возможность.")
                return False
        return True

    def before_reaction(self, target, battle_map):
        self.owner.use_skills(
            skill_type=ACTIVATE_BEFORE_STRIKE,
            target=target, battle_map=battle_map
        )
        target.use_skills(
            skill_type=ACTIVATE_BEFORE_GET_HIT,
            target=self.owner, battle_map=battle_map
        )

    def after_reaction(self, target, damage, kills, battle_map):
        self.owner.use_skills(
            skill_type=ACTIVATE_AFTER_STRIKE,
            target=target, damage=damage,
            kills=kills, battle_map=battle_map
        )
        target.use_skills(
            skill_type=ACTIVATE_AFTER_GET_HIT,
            target=self.owner, damage=damage,
            kills=kills, battle_map=battle_map
        )
        self.owner.apply_effect(BlockCounter())

    def failed_counter(self):
        failed = False
        for number, effect in enumerate(self.owner.effects):
            if TEMPORARY_BLOCK_COUNTER in effect.special_effects:
                failed = True
                break
        if failed:
            self.owner.dispell_by_case(DISPELL_TEMPORARY_BLOCK_COUNTER)
            return True
        else:
            return False


class InfiniteMeleeCounter(MeleeCounter):

    def after_reaction(self, target, damage, kills, battle_map):
        self.owner.use_skills(
            ACTIVATE_AFTER_STRIKE, target, damage, kills, battle_map
        )
        target.use_skills(
            skill_type=ACTIVATE_AFTER_GET_HIT,
            target=self.owner, damage=damage,
            kills=kills, battle_map=battle_map
        )


class BattleFrenzyCounter(MeleeCounter):

    def after_reaction(self, target, damage, kills, battle_map):
        self.owner.use_skills(
            skill_type=ACTIVATE_AFTER_STRIKE,
            target=target, damage=damage,
            kills=kills, battle_map=battle_map
        )
        target.use_skills(
            skill_type=ACTIVATE_AFTER_GET_HIT,
            target=self.owner, damage=damage,
            kills=kills, battle_map=battle_map
        )
        self.owner.apply_effect(BattleFrenzy())

    def calculate_damage_modifier(self):
        damage_modifier = 1
        for effect in self.owner.effects:
            for k, v in effect.modifiers.items():
                if (
                        k == BATTLE_FRENZY_MODIFIER and
                        v > damage_modifier
                ):
                    damage_modifier = v
        damage_modifier = damage_modifier * self.luck_modifier()
        return damage_modifier


class WeakMeleeCounter(MeleeCounter):

    def calculate_damage_modifier(self):
        damage_modifier = 0.5 * self.luck_modifier()
        return damage_modifier


class AcidBlood(Reaction):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Кислотная кровь"
        self.owner = owner
        self.keyword = MELEE_COUNTER

    def react(self, target, battle_map):
        self.strike(target, battle_map)

    def strike(self, target, battle_map):
        if check_ghost(target):
            return
        damage_modifier = 0.25
        min_damage = int(
            self.owner.min_damage * self.owner.quantity *
            damage_modifier
        )
        max_damage = int(
            self.owner.max_damage * self.owner.quantity *
            damage_modifier
        )
        damage = calculate_damage(
            damage=randint(min_damage, max_damage),
            attack=self.owner.attack,
            defence=target.defence,
            max_damage=target.hp
        )
        kills = target.take_damage(damage)
        print(f"{self.owner.name} брызжет кислотной "
              f"кровью на  {target.name}. "
              f"Наносит {damage} урона. "
              f"Погибло {kills} {target.name}. "
              f"Осталось {target.quantity}")


class Coward(Reaction):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Трус"
        self.owner = owner
        self.keyword = MELEE_COUNTER

    def react(self, target, battle_map):
        if not self.can_unit_react(target, battle_map):
            return
        run_away(battle_map=battle_map,
                 scary_unit=target, coward=self.owner)

    def can_unit_react(self, target, battle_map):
        if not self.owner.hp > 0:
            print(f"{self.owner.name} не может реагировать т.к. мертв")
            return False
        if target.hp == 0:
            print(f"{self.owner.name} не может действовать т.к. "
                  f"цель мертва.")
            return False
        return True


class RunAndShoot(MeleeCounter):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Беги и стреляй"
        self.owner = owner
        self.keyword = MELEE_COUNTER

    def react(self, target, battle_map):
        run_away(
            battle_map=battle_map, scary_unit=target, coward=self.owner
        )
        if not self.can_unit_react(target, battle_map):
            return
        if self.failed_counter():
            return
        self.shoot(target, battle_map)

    def shoot(self, target, battle_map):
        if check_ghost(target):
            return
        # Половинный удар + стандартный расчет удачи
        damage_modifier = 0.5 * self.calculate_damage_modifier()
        min_damage = int(
            self.owner.min_damage * self.owner.quantity *
            damage_modifier
        )
        max_damage = int(
            self.owner.max_damage * self.owner.quantity *
            damage_modifier
        )
        damage = calculate_damage(
            damage=randint(min_damage, max_damage),
            attack=self.owner.attack,
            defence=target.defence,
            max_damage=target.hp
        )
        self.before_reaction(target, battle_map)
        kills = target.take_damage(damage)
        self.after_reaction(target, damage, kills, battle_map)
        print(f"{self.owner.name} стреляет в {target.name}. "
              f"Наносит {damage} урона. "
              f"Погибло {kills} {target.name}. "
              f"Осталось {target.quantity}")

    def before_reaction(self, target, battle_map):
        self.owner.use_skills(
            skill_type=ACTIVATE_BEFORE_SHOOT,
            target=target, battle_map=battle_map
        )
        target.use_skills(
            skill_type=ACTIVATE_BEFORE_GET_SHOT,
            target=self.owner, battle_map=battle_map
        )

    def after_reaction(self, target, damage, kills, battle_map):
        self.owner.use_skills(
            skill_type=ACTIVATE_AFTER_SHOOT,
            target=target, damage=damage,
            kills=kills, battle_map=battle_map
        )
        target.use_skills(
            skill_type=ACTIVATE_AFTER_GET_SHOT,
            target=self.owner, damage=damage,
            kills=kills, battle_map=battle_map
        )
        self.owner.apply_effect(BlockCounter())


class DoubleDamageMeleeCounter(MeleeCounter):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Свирепое возмездие"

    def calculate_damage_modifier(self):
        return 2*super().calculate_damage_modifier()
