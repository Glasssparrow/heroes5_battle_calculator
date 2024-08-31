from .initiative.initiative_handler import Initiative
from .turn.turm_simulator import TurnSimulator
from .battle_map.battle_map import BattleMap


def battle(unit1, unit2, turn_limit):
    units = [unit1, unit2]
    initiative_system = Initiative(units)
    battle_map = BattleMap(10, 12)
    simulation = TurnSimulator(units, battle_map)
    for turn in range(turn_limit):
        active_unit = initiative_system.get_active_unit()
        simulation.next_turn(active_unit)
    return unit1
