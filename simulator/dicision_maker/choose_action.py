from .get_positions import (
    get_melee_attack_positions,
    get_range_attack_positions
)
from .get_danger_zone import get_danger_zone


def choose_action(unit, battle_map):
    melee_attacks = get_melee_attack_positions(unit, battle_map)
    range_attacks = get_range_attack_positions(unit, battle_map)
    danger_zone = get_danger_zone(unit, battle_map)
    if not melee_attacks and not range_attacks:
        pass
    return 0
