from ..battle_map.battle_map import BattleMap


class TurnSimulator:

    def __init__(self, units: list, battle_map: BattleMap):
        self.units = units
        self.map = battle_map
        self.units[0].color = "Красный"
        self.units[1].color = "Синий"

    def next_turn(self, active_unit):
        pass
