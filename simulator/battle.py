from .initiative.initiative_handler import Initiative


def battle(unit1, unit2, turn_limit):
    units = [unit1, unit2]
    initiative_system = Initiative(units)
    for turn in range(turn_limit):
        active_unit = initiative_system.get_active_unit()
    return unit1
