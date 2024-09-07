

def choose_target(active_unit, action, battle_map):
    for unit in battle_map.units:
        if unit.id != active_unit.id:
            return unit
    return None  # Возвращает None, если не атакуем
