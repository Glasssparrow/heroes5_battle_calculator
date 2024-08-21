from tournament_manager.duel import just_1vs1


def tournament_order():
    winner = just_1vs1(
        "Манекен1",
        "Манекен2",
        100, 100,
        0
    )
    print(f'winner is "{winner}"')
