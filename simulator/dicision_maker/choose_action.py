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
    danger_zone = get_danger_zone(the_unit, battle_map)
    if not melee_attacks and not range_attacks:
        pass
    return 0
