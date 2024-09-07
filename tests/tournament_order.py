from tournament_manager.just_1vs1 import just_1vs1


def tournament_order():
    winner = just_1vs1(
        "Манекен",
        "Пугало",
        100, 100,
        0,
        1,
        3,
    )
    print(f'Манекен1 have {winner*100}% chance to win')
