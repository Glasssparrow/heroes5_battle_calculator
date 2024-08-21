from tournament_manager.duel import duel


def tournament_order():
    winner = duel(
        "Манекен1",
        "Манекен2",
        100, 100,
        0
    )
    print(f'winner is "{winner}"')
