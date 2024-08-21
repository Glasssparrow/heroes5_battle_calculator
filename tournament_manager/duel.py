

def duel(
        first_unit_name: str,
        second_unit_name: str,
        first_unit_quantity: int,
        second_unit_quantity: int,
        type_of_quantity: int,
):
    """
    :param first_unit_name: name for database
    :param second_unit_name: name for database
    :param first_unit_quantity: of soldiers/gold/weeks
    :param second_unit_quantity: of soldiers/gold/weeks
    :param type_of_quantity: 0: quantity
    :return: name of winner
    """
    print(
        f"Duel!\n"
        f"{first_unit_name}x{first_unit_quantity}vs"
        f"{second_unit_name}x{second_unit_quantity}.\n"
        f"Type of duel - {type_of_quantity}."
    )
    return "Duel is fake!"
