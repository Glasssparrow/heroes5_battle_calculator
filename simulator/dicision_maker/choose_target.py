from ..simulator_keywords import (
    MELEE_ACTION,
    JUST_MOVEMENT,
)


def choose_target(active_unit, action, battle_map):
    if action.type_of_action == MELEE_ACTION:
        for unit in battle_map.units:
            if unit.id != active_unit.id:
                return unit
    elif action.type_of_action == JUST_MOVEMENT:
        return None  # Возвращает None, если не атакуем
    else:
        raise Exception("Не найден тип действия")
