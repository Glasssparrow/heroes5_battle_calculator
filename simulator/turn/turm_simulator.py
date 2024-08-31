from ..battle_map.battle_map import BattleMap


class TurnSimulator:

    def __init__(self, units: list, battle_map: BattleMap):
        self.units = units
        self.map = battle_map
        self.map.add_unit(
            unit=self.units[0],
            x=0, y=5,
            color=self.units[0].color,
        )
        self.map.add_unit(
            unit=self.units[0],
            x=11, y=5,
            color=self.units[0].color,
        )

    def next_turn(self, active_unit):
        pass
