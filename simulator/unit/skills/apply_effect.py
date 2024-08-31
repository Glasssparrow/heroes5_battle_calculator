from .common import Skill, calculate_base_chance
from ..common import check_random
from ..effects import *
from simulator.simulator_keywords import *
from random import choice


class PeasantBash(Skill):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Оглушение (крестьяне)"
        self.activation_cases.append(ACTIVATE_BEFORE_STRIKE)

    def use(self, target, damage, kills, battle_map):
        if (
            check_random(self.get_chance(target))
        ):
            target.apply_effect(Block1Counterattack())
            target.apply_effect(Bash())

    @staticmethod
    def _chance_formula(base_chance):
        return 1-(1-base_chance)**1

    def get_chance(self, target):
        chance = self._chance_formula(
            calculate_base_chance(self.owner, target)
        )
        if chance < 0:
            return 0
        elif chance > 1:
            return 1
        else:
            return chance


class FootmanBash(PeasantBash):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Оглушение (мечники)"

    @staticmethod
    def _chance_formula(base_chance):
        return 1-(1-base_chance)**1.5


class CyclopeBash(PeasantBash):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Оглушение (циклопы)"

    def use(self, target, damage, kills, battle_map):
        if (
            check_random(self.get_chance(target))
        ):
            target.apply_effect(Bash())

    @staticmethod
    def _chance_formula(base_chance):
        return 1-(1-base_chance)**0.8


class BlindingStrike(PeasantBash):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Ослепляющий удар"

    def use(self, target, damage, kills, battle_map):
        if (
            check_random(self.get_chance(target)) and
            not target.check_immunity(BLIND_IMMUNE)
        ):
            target.apply_effect(BlindFromStrike())
        else:
            if target.check_immunity(BLIND_IMMUNE):
                print(f"{target.name} иммунитет ослеплению")
            else:
                print(f"Ослепляющий удар не сработал")

    @staticmethod
    def _chance_formula(base_chance):
        return 1-(1-base_chance)**1


class BlindingStrikeVampires(BlindingStrike):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Ослепляющий удар (вампиры)"

    @staticmethod
    def _chance_formula(base_chance):
        return 1 - (1 - base_chance) ** 3


class PlagueStrike(Skill):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Чумной удар"
        self.activation_cases.append(ACTIVATE_AFTER_STRIKE)

    @staticmethod
    def use(target, damage, kills, battle_map):
        target.apply_effect(Plague())


class ApplySorrow(Skill):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Скорбный удар"
        self.activation_cases.append(ACTIVATE_AFTER_STRIKE)

    @staticmethod
    def use(target, damage, kills, battle_map):
        target.apply_effect(Sorrow())


class ApplyWeakening(Skill):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Ослабляющий удар"
        self.activation_cases.append(ACTIVATE_AFTER_STRIKE)

    @staticmethod
    def use(target, damage, kills, battle_map):
        target.apply_effect(WeakeningNoSkill())


class ApplyPoison(Skill):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Отравляющий удар"
        self.activation_cases = [
            ACTIVATE_AFTER_STRIKE, ACTIVATE_AFTER_SHOOT
        ]

    def use(self, target, damage, kills, battle_map):
        target.apply_effect(Poison(self.owner.quantity))


class WyvernPoison(ApplyPoison):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Яд виверны"

    def use(self, target, damage, kills, battle_map):
        target.apply_effect(Poison(self.owner.quantity*4))


class Whip(Skill):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Удар хлыстом"
        self.activation_cases.append(ACTIVATE_AFTER_STRIKE)

    @staticmethod
    def use(target, damage, kills, battle_map):
        effect = choice((SlowAdvanced, WeakeningAdvanced, Berserk))
        target.apply_effect(effect())


class MagicStrike(Skill):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Колдовской удар"
        self.activation_cases.append(ACTIVATE_AFTER_STRIKE)

    @staticmethod
    def use(target, damage, kills, battle_map):
        effect = choice((
            WeakeningExpert, SlowExpert,
            AttackDebuffExpert, DefenceDebuffExpert,
        ))
        target.apply_effect(effect())


class ApplyBadLuck(Skill):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Наложение невезения"
        self.activation_cases.append(ACTIVATE_AFTER_STRIKE)

    @staticmethod
    def use(target, damage, kills, battle_map):
        target.apply_effect(BadLuck())
