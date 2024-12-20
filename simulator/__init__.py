from .unit.unit import Unit
from .unit.actions import *


__main__ = [
    "Unit",  # Класс юнита, при создании не имеет навыков и особенностей.

    # Действия.
    # Ближний бой.
    "Melee",  # Обычная атака
    "WeakMelee",  # Слабая (50% урона) атака
    "DoubleAttackIfKill",  # атака, затем еще одна (если убито минимум 1 сущ.)
    "DoubleAttack",  # атака, затем еще одна
    "Assault",  # атака, затем шанс на еще одну атаку
    "LizardCharge",  # атака с бонусом к АТК за пройденные клетки
    "ChivalryCharge",  # атака с бонусом УРН за пройденные клетки
    "MeleeNoCounter",  # атака на которую враг не отвечает
    "MeleeNoCounterIfSlowed",  # атака на которую враг не отвечает если замедлен
    # Движение
    "Movement",
]
