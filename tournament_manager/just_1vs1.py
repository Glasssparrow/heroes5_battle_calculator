from read_database.read_database import (
    read_data
)
from referee.duel import duel


def just_1vs1(
        first_unit_name: str,
        second_unit_name: str,
        first_unit_quantity: int,
        second_unit_quantity: int,
        type_of_quantity: int,
        rounds: int,
        turn_limit: int,
):
    """
    :param first_unit_name: name for the database.
    :param second_unit_name: name for the database.
    :param first_unit_quantity: of soldiers/gold/weeks.
    :param second_unit_quantity: of soldiers/gold/weeks.
    :param type_of_quantity: 0: quantity.
    :param rounds: how many battles to simulate.
    :param turn_limit: how long can the battle lasts.
    :return: chance of victory for the first unit.
    """
    data = read_data()
    chance_of_winning = duel(
        first_unit_name,
        second_unit_name,
        first_unit_quantity,
        second_unit_quantity,
        type_of_quantity,
        rounds,
        turn_limit,
        data,
    )
    print(
        f"Duel!\n"
        f"{first_unit_name}x{first_unit_quantity}vs"
        f"{second_unit_name}x{second_unit_quantity}.\n"
        f"Type of duel - {type_of_quantity}."
    )
    return chance_of_winning
