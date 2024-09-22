from .get_positions import (
    get_melee_attack_positions,
    get_range_attack_positions
)
from .get_danger_zone import get_danger_zone
from .common import get_hostile_units


def choose_action(the_unit, battle_map):
    enemy_units = get_hostile_units(the_unit, battle_map)
    melee_attacks = get_melee_attack_positions(the_unit, battle_map)
    range_attacks = get_range_attack_positions(the_unit, battle_map)
    # Выбор действия с наибольшей угрозой.
    action = None  # Номер действия в листе действий экземпляра Unit
    threat = 0
    for attack_position in melee_attacks:
        if not action:
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
    elif False:
        # Выбор между атакой и выходом из опасной зоны.
        # TODO
        pass
    else:
        # Если может атаковать, то атакуем с точки наименьшей угрозы.
        pass
    return 0
