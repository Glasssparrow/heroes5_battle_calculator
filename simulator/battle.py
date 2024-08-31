from .initiative.initiative_handler import Initiative


def battle(unit1, unit2):
    initiative_system = Initiative([unit1, unit2])
    active_unit = initiative_system.get_active_unit()
    return unit1
