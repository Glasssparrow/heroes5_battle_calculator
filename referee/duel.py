from read_database.read_database import (
    DataBase
)


def duel(
    first_unit_name: str,
    second_unit_name: str,
    first_unit_quantity: int,
    second_unit_quantity: int,
    type_of_quantity: int,
    rounds: int,
    database: DataBase,
):
    """
    :param first_unit_name: name for the database.
    :param second_unit_name: name for the database.
    :param first_unit_quantity: of soldiers/gold/weeks.
    :param second_unit_quantity: of soldiers/gold/weeks.
    :param type_of_quantity: 0: quantity.
    :param rounds: how many battles to simulate.
    :param database: look read_database package.
    :return: chance of victory for first unit.
    """
    wins_unit1 = 0
    for num in range(rounds):
        wins_unit1 += 1
    chance = round(wins_unit1/rounds, 3)
    return chance