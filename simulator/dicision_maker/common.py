

def get_hostile_units(the_unit, battle_map):
    enemy_units = []
    for unit in battle_map.units:
        if unit.color != the_unit.color:
            enemy_units.append(unit)
    return enemy_units
