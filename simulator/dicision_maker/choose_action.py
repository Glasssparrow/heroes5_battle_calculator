from .get_positions import (
    get_melee_attack_positions,
    get_range_attack_positions
)
from .get_danger_zone import get_danger_zone
from .common import get_hostile_units
from .choose_target import choose_target


class Decision:

    def __init__(self, action_id, action, chosen_position, target):
        # Выбранное действие
        self.action_id = action_id
        self.action = action
        # Позиция с которой действие будет применено.
        self.chosen_position = chosen_position
        # Цель навыка
        self.target = target


def choose_action(the_unit, battle_map):
    enemy_units = get_hostile_units(the_unit, battle_map)
    melee_attacks = get_melee_attack_positions(the_unit, battle_map)
    range_attacks = get_range_attack_positions(the_unit, battle_map)
    # attack.positions - лист координат (х, у,),
    # с которых можно атаковать.

    # Выбор действия с наибольшей угрозой.
    action_index = None  # Номер действия в листе действий экземпляра Unit
    threat = 0
    # Выбираем действие с наибольшим уровнем угрозы
    # (из тех что можно применить).
    for pos_for_action in melee_attacks:
        # Если действие не выбрано, берем первое попавшееся.
        if not action_index:
            action_index = pos_for_action.action_index
            continue
        if pos_for_action.action.threat > threat:
            action_index = pos_for_action.action_index
            threat = pos_for_action.action.threat
    for pos_for_action in range_attacks:
        if pos_for_action.action.threat > threat:
            action_index = pos_for_action.action_index
            threat = pos_for_action.action.threat
    danger_zone = get_danger_zone(enemy_units[0], battle_map)
    if not melee_attacks and not range_attacks:
        # Если не может атаковать, выбрать клетку для перемещения.
        pass
    # TODO
    # Выбор между атакой и выходом из опасной зоны.
    else:
        # Если может атаковать, то атакуем с точки наименьшей угрозы.
        pass
    return 0
