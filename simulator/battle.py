from .initiative.initiative_handler import Initiative


def battle(unit1, unit2, turn_limit):
    initiative_system = Initiative([unit1, unit2])
    for turn in range(turn_limit):
        active_unit = initiative_system.get_active_unit()
    return unit1
