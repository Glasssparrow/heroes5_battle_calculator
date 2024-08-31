from math import ceil
from .stats import *
from .skills.turnend import *
from .skills.game_mechanics import *


# Класс отвечающий за взаимодействие между юнитами.
# Не отвечает за шкалу инициативы и передвижение.
# Экземпляры класса лишь хранят положение на поле и шкале инициативы.
# Наложение аур связано с передвижением, поэтому также обрабатывается вне
# класса.
class Unit:

    attack = Stat()
    defence = Stat()
    min_damage = MinDamage()
    max_damage = MaxDamage()
    health = Health()
    initiative = Initiative()
    speed = Speed()
    luck = Luck()
    morale = Morale()

    def __init__(self, name,
                 attack, defence, min_damage, max_damage, health,
                 initiative, speed, mana, ammo,
                 color=DEFAULT_COLOR,
                 ):
        self.name = name
        self.color = color
        self.side = 0
        self.id = None
        self.coord = None
        self.pos = None

        self.actions = []
        self.reactions = []
        self.skills = [DispellAfterTakingDamage(self)]
        self.turnend_skills = [HighMorale(owner=self),
                               LowMorale(owner=self)]
        self.auras = []
        self.effects = []
        self.immunities = []
        self.special_attributes = []  # Призрак, Стена_щитов
        self.attack = attack
        self.defence = defence
        self.min_damage = min_damage
        self.max_damage = max_damage
        self._health = health
        self.initiative = initiative
        self.speed = speed
        self._max_quantity = 0
        self.quantity = 0
        self.hp = 0
        self.luck = 0
        self.morale = 0
        self.big = False

        self.max_mana = mana
        self.mana = mana
        self.max_ammo = ammo
        self.ammo = ammo

        self.tiles_moved = 0

    def take_action(self, action_type, target, battle_map):
        self.start_turn()
        self._action(action_type, target, battle_map)
        self.end_turn()

    def start_turn(self):
        self.dispell_by_case(DISPELL_AT_TURN_START)
        for skill in self.turnend_skills:
            if ACTIVATE_AT_TURN_START in skill.activation_cases:
                skill.use()
                return

    def _action(self, action_type, target, battle_map):
        for action in self.actions:
            if action.keyword == action_type:
                action.act(target, battle_map)
                return

    def use_aura(self, target, distance):
        pass

    def end_turn(self):
        self.dispell_by_case(DISPELL_AT_TURN_END)
        for skill in self.turnend_skills:
            if ACTIVATE_AT_TURN_END in skill.activation_cases:
                skill.use()
        for effect in self.effects:
            for k, v in effect.modifiers.items():
                if k == POISON:
                    kills = self.take_damage(v)
                    print(f"{self.name} получает {v} урона от яда. "
                          f"Погибло {kills} существ. Осталось "
                          f"{self.quantity}")
        self.tiles_moved = 0  # После срабатывания всех эффектов

    def react(self, reaction_type, target, battle_map):
        for reaction in self.reactions:
            if reaction.keyword == reaction_type:
                reaction.react(target, battle_map)

    def use_skills(
            self, skill_type, target, battle_map, damage=0, kills=0
    ):
        for skill in self.skills:
            if skill_type in skill.activation_cases:
                skill.use(target, damage, kills, battle_map)

    def apply_effect(self, new_effect):
        for immunity in new_effect.blocked_by_immunities:
            if immunity in self.immunities:
                print(f"{self.name} имеет иммунитет к {new_effect.name}")
                return
        for effect in self.effects:
            if new_effect.name == effect.name:
                effect.reapply(new_effect)
                print(f"На {self.name} переналожен эффект "
                      f"{effect.name}")
                return
        print(f"На {self.name} наложен эффект {new_effect.name}")
        self.effects.append(new_effect)

    def take_damage(self, damage):
        self.hp = self.hp - damage
        if self.hp < 0:
            self.hp = 0
        quantity_before = self.quantity
        self.quantity = ceil(self.hp / self.health)
        kills = quantity_before - self.quantity
        return kills

    def take_healing(self, healing):
        self.hp = self.hp + healing
        if self.hp > self._max_quantity * self.health:
            self.hp = self._max_quantity * self.health
        quantity_before = self.quantity
        self.quantity = self.hp / self.health
        revived = self.quantity - quantity_before
        return revived

    def get_quantity(self, quantity):
        self._max_quantity = quantity
        self.quantity = quantity
        self.hp = quantity * self.health

    def add_action(self, action):
        self.actions.append(action(self))

    def add_reaction(self, reaction):
        self.reactions.append(reaction(self))

    def add_skill(self, skill):
        self.skills.append(skill(self))

    def add_turnend_skill(self, skill):
        self.turnend_skills.append(skill(self))

    def add_aura(self, aura):
        self.auras.append(aura)

    def dispell_by_case(self, dispell_trigger):
        for_delete = []
        for number, effect in enumerate(self.effects):
            if dispell_trigger in effect.dispell_conditions:
                if effect.dispell_exception_once:
                    print(f"Использован 1 жетон иммунитета к снятию "
                          f"{effect.name}")
                    effect.dispell_exception_once = False
                else:
                    for_delete.append(number)
        for x in reversed(for_delete):
            print(f"{self.name}. Эффект {self.effects[x].name} снят")
            self.effects.pop(x)

    def check_immunity(self, immunity_keyword):
        if not self.immunities:
            return False
        for immunity in self.immunities:
            if immunity == immunity_keyword:
                return True
        return False
