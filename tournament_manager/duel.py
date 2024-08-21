

def duel(
        first_unit_name: str,
        second_unit_name: str,
        first_unit_quantity: int,
        second_unit_quantity: int,
        type_of_quantity: int,
):
    print(
        f"Duel!\n"
        f"{first_unit_name}x{first_unit_quantity}vs"
        f"{second_unit_name}x{second_unit_quantity}.\n"
        f"Type of duel - {type_of_quantity}."
    )
