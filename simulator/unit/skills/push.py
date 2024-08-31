from .common import calculate_base_chance
from ..common import check_random
from ..effects import *
from ..simulator_keywords import *
from .apply_effect import PeasantBash
from ..requirements import push, run_away


class BearPush(PeasantBash):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Удар лапой"
        self.activation_cases.append(ACTIVATE_AFTER_STRIKE)

    def use(self, target, damage, kills, battle_map):
        if (
            check_random(self.get_chance(target)) and
            not target.check_immunity(PUSH_IMMUNE)
        ):
            target.apply_effect(Bash())
            push(battle_map, self.owner, target)
        else:
            print(f"У {target.name} иммунитет к отталкиванию")

    def _chance_formula(self, base_chance):
        return 1-(1-base_chance)**self.owner.tiles_moved


class BearRoar(PeasantBash):

    def __init__(self, owner):
        super().__init__(owner)
        self.name = "Медвежий рёв"
        self.activation_cases.append(ACTIVATE_AFTER_STRIKE)

    def use(self, target, damage, kills, battle_map):
        if (
                check_random(self.get_chance(target)) and
                not target.check_immunity(FEAR_IMMUNE)
        ):
            target.apply_effect(Bash())
            run_away(battle_map, self.owner, target)
        else:
            print(f"У {target.name} иммунитет к запугиванию")

    @staticmethod
    def _roar_chance(base_chance, target):
        if target.big:
            return 1-(1-base_chance)**0.9
        else:
            return 0.5+(1-(1-base_chance)**0.9)/2

    def get_chance(self, target):
        chance = self._roar_chance(
            calculate_base_chance(self.owner, target),
            target,
        )
        if chance < 0:
            return 0
        elif chance > 1:
            return 1
        else:
            return chance
