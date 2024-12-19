from ..battle_map.get_distance import get_distance
from .common import get_hostile_units
from ..simulator_keywords import (
    MELEE_ACTIONS,  # Лист действий ближнего боя
    MELEE_ACTION,  # ближний бой
    MELEE_SPELL,  # ближний бой без возможности двигаться
    HIT_AND_RUN_ACTION,  # Атака с возвратом на исходную позицию
)


class AttackPositionsForAction:
    def __init__(self, action_index, action):
        self.positions = []
        self.action_name = action.name
        self.action_index = action_index  # position in unit's actions list.
        self.action_threat_lvl = action.threat

    def add_coord(self, coord):
        self.positions.append((coord[0], coord[1]))


class AttackPositions:
    def __init__(self):
        self.positions = []
        self.enemies_in_range = {}

    def add_coord(self, x, y):
        self.positions.append((x,y))
        self.enemies_in_range[f"{x}:{y}"] = []

    def add_unit_to_coord(self, x, y, unit):
        if (x,y) not in self.positions:
            raise Exception(f"{x,y} не найдено в списке коорд.")
        self.enemies_in_range[f"{x}:{y}"].append(unit)


def get_melee_attack_positions(the_unit, battle_map):
    positions_for_melee_actions = []
    available_cells = battle_map.get_available_cells(the_unit)
    enemy_units = get_hostile_units(the_unit, battle_map)

    # Находим все точки с которых можно ударить после движения.
    attack_positions = []
    for (x, y), length, path in available_cells:
        for enemy in enemy_units:
            if get_distance(
                    coord1=(x, y),
                    is_big1=the_unit.big,
                    coord2=(enemy.coord[0], enemy.coord[1]),
                    is_big2=enemy.big,
            ) == 1:
                attack_positions.append((x, y))

    # Заполняем лист positions_for_melee_actions
    for action_index, action in enumerate(the_unit.actions):
        # Атаки после движения
        if (
            action.type_of_action in MELEE_ACTIONS and
            action.type_of_action != MELEE_SPELL
        ):
            attack_position = AttackPositionsForAction(
                action_index=action_index,
                action=action,
            )
            positions_for_melee_actions.append(attack_position)
            for x, y in attack_positions:
                attack_position.add_coord((x, y,))
            if (
                action.type_of_action == HIT_AND_RUN_ACTION and
                the_unit.coord not in attack_positions
            ):
                attack_position.add_coord(
                    coord=(the_unit.coord[0], the_unit.coord[1],),
                )
        # Если можем ударить с места, то включаем
        # навыки ближнего боя, которые можно применить только с места.
        elif (
            action.type_of_action == MELEE_SPELL and
            the_unit.coord in attack_positions
        ):
            attack_position = AttackPositionsForAction(
                action_index=action_index,
                action=action,
            )
            positions_for_melee_actions.append(attack_position)
            attack_position.add_coord(
                coord=(the_unit.coord[0], the_unit.coord[1],),
            )
        # Если это не навык ближнего боя - пропускаем.
        else:
            continue
    return positions_for_melee_actions


def get_range_attack_positions(unit, battle_map):
    attack_positions = []
    return attack_positions
