from read_database.read_database import (
    DataBase
)
from simulator.battle import battle


def duel(
    first_unit_name: str,
    second_unit_name: str,
    first_unit_quantity: int,
    second_unit_quantity: int,
    type_of_quantity: int,
    rounds: int,
    turn_limit: int,
    database: DataBase,
):
    """
    :param first_unit_name: name for the database.
    :param second_unit_name: name for the database.
    :param first_unit_quantity: of soldiers/gold/weeks.
    :param second_unit_quantity: of soldiers/gold/weeks.
    :param type_of_quantity: 0: quantity.
    :param rounds: how many battles to simulate.
    :param turn_limit: how long can the battle lasts.
    :param database: look read_database package.
    :return: chance of victory for first unit.
    """
    wins_unit1 = 0
    for num in range(rounds):
        unit1 = database.get_unit(first_unit_name)
        unit1.set_quantity(first_unit_quantity)
        unit1.color = "Красный"
        unit2 = database.get_unit(second_unit_name)
        unit2.set_quantity(second_unit_quantity)
        unit2.color = "Синий"
        winner = battle(unit1, unit2, turn_limit)
        if winner.id == unit1.id:
            wins_unit1 += 1

    chance = round(wins_unit1/rounds, 3)
    return chance
