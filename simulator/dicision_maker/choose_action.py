from .get_positions import (
    get_melee_attack_positions,
    get_range_attack_positions
)
from .get_danger_zone import get_danger_zone
from .common import get_hostile_units


class Decision:

    def __init__(self, action_id):
        self.action_id = action_id
        self.action = None
        self.positions = []
        self.chosen_position = None


def choose_action(the_unit, battle_map):
    # Выбирает действие, которое будет применять юнит.
    # Перемещение это тоже действие.
    # TODO
    # Также выбирает клетку с которой должно выполниться действие.
    enemy_units = get_hostile_units(the_unit, battle_map)
    melee_attacks = get_melee_attack_positions(the_unit, battle_map)
    range_attacks = get_range_attack_positions(the_unit, battle_map)
    # Выбор действия с наибольшей угрозой.
    action = None  # Номер действия в листе действий экземпляра Unit
    threat = 0
    # Выбираем действие с наибольшим уровнем угрозы (из тех что можно применить).
    for attack_position in melee_attacks:
        if not action:  # Если действие не выбрано, берем первое попавшееся.
            action = attack_position.action_index
            continue
        if attack_position.action.threat > threat:
            action = attack_position.action_index
            threat = attack_position.action.threat
    for attack_position in range_attacks:
        if attack_position.action.threat > threat:
            action = attack_position.action_index
            threat = attack_position.action.threat
    danger_zone = get_danger_zone(enemy_units[0], battle_map)
    if not melee_attacks and not range_attacks:
        # Если не может атаковать, выбрать клетку
        # для перемещения.
        pass
    # TODO
    # Выбор между атакой и выходом из опасной зоны.
    else:
        # Если может атаковать, то атакуем с точки наименьшей угрозы.
        pass
    return 0
