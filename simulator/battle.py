from .initiative.initiative_handler import Initiative
from .turn.turm_simulator import TurnSimulator
from .battle_map.battle_map import BattleMap


def battle(unit1, unit2, turn_limit):
    units = [unit1, unit2]
    initiative_system = Initiative(units)
    # создаем карту и размещаем на ней юниты
    battle_map = BattleMap(10, 12)
    battle_map.add_unit(
        unit=unit1,
        x=2, y=2,
        color="Синий",
    )
    battle_map.add_unit(
        unit=unit2,
        x=8, y=8,
        color="Красный",
    )
    battle_map.create_pathfinders()  # Подготавливаем карту к работе.
    # Подготавливаем симулятор
    simulation = TurnSimulator(units, battle_map)
    # Рассчитываем заданное количество ходов.
    for turn in range(turn_limit):
        active_unit = initiative_system.get_active_unit()
        simulation.next_turn(active_unit)
    if unit1.how_healthy() > unit2.how_healthy():
        return unit1
    else:
        return unit2
