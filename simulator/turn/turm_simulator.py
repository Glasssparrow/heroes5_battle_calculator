from ..battle_map.battle_map import BattleMap
from ..dicision_maker.choose_action import choose_action


class TurnSimulator:

    def __init__(self, units: list, battle_map: BattleMap):
        self.units = units
        self.map = battle_map
        self.map.add_unit(
            unit=self.units[0],
            x=0, y=5,
        )
        self.map.add_unit(
            unit=self.units[0],
            x=11, y=5,
        )

    def next_turn(self, active_unit):
        active_unit.start_turn()
        action = choose_action(active_unit)
        active_unit.end_turn()
