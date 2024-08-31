from .common import Effect
from simulator.simulator_keywords import *


class Berserk(Effect):

    def __init__(self):
        super().__init__()
        self.name = "Берсерк"
        self.time = 3


class SlowNoSkill(Effect):

    def __init__(self):
        super().__init__()
        self.name = "Замедление (нет навыка)"
        self.initiative = -0.25
        self.time = 3


class SlowBasics(Effect):

    def __init__(self):
        super().__init__()
        self.name = "Замедление (основы)"
        self.initiative = -0.3
        self.time = 3


class SlowAdvanced(Effect):

    def __init__(self):
        super().__init__()
        self.name = "Замедление (сильная)"
        self.initiative = -0.35
        self.time = 3


class SlowExpert(Effect):

    def __init__(self):
        super().__init__()
        self.name = "Замедление (эксперт)"
        self.initiative = -0.4
        self.time = 3


class Sorrow(Effect):

    def __init__(self):
        super().__init__()
        self.name = "скорбь"
        self.morale = -2
        self.luck = -2
        self.time = 3


class WeakeningNoSkill(Effect):

    def __init__(self):
        super().__init__()
        self.name = "ослабление (нет навыка)"
        self.damage = -0.5
        self.time = 3


class WeakeningBasics(Effect):

    def __init__(self):
        super().__init__()
        self.name = "ослабление (основы)"
        self.damage = -0.65
        self.time = 3


class WeakeningAdvanced(Effect):

    def __init__(self):
        super().__init__()
        self.name = "ослабление (сильная)"
        self.damage = -0.8
        self.time = 3


class WeakeningExpert(Effect):

    def __init__(self):
        super().__init__()
        self.name = "ослабление (эксперт)"
        self.damage = -1
        self.time = 3


class Blind(Effect):

    def __init__(self):
        super().__init__()
        self.name = "ослепление"
        self.special_effects.append(BLOCK_ACTION)
        self.special_effects.append(BLOCK_COUNTER)
        self.dispell_conditions.append(DISPELL_AFTER_TAKING_DAMAGE)


class AttackDebuffNoSkill(Effect):

    def __init__(self):
        super().__init__()
        self.name = "немощность (нет навыка)"
        self.attack = -3
        self.time = 3


class AttackDebuffBasics(Effect):

    def __init__(self):
        super().__init__()
        self.name = "немощность (основы)"
        self.attack = -6
        self.time = 3


class AttackDebuffAdvanced(Effect):

    def __init__(self):
        super().__init__()
        self.name = "немощность (сильная)"
        self.attack = -9
        self.time = 3


class AttackDebuffExpert(Effect):

    def __init__(self):
        super().__init__()
        self.name = "немощность (эксперт)"
        self.attack = -12
        self.time = 3


class DefenceDebuffNoSkill(Effect):

    def __init__(self):
        super().__init__()
        self.name = "разрушающий луч (нет навыка)"
        self.defence = -3

    def reapply(self, new_instance):
        self.defence += new_instance.defence


class DefenceDebuffBasics(DefenceDebuffNoSkill):

    def __init__(self):
        super().__init__()
        self.name = "разрушающий луч (основы)"
        self.defence = -4


class DefenceDebuffAdvanced(DefenceDebuffNoSkill):

    def __init__(self):
        super().__init__()
        self.name = "разрушающий луч (сильная)"
        self.defence = -5


class DefenceDebuffExpert(DefenceDebuffNoSkill):

    def __init__(self):
        super().__init__()
        self.name = "разрушающий луч (эксперт)"
        self.defence = -6
