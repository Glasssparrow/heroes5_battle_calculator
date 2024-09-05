from .get_positions import (
    get_melee_attack_positions,
    get_range_attack_positions
)


def choose_action(unit):
    melee_attacks = get_melee_attack_positions()
    range_attacks = get_range_attack_positions()
