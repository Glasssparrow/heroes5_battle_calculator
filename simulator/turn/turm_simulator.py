from ..battle_map.battle_map import BattleMap
from ..dicision_maker.choose_action import choose_action


class TurnSimulator:

    def __init__(self, units: list, battle_map: BattleMap):
        self.units = units
        self.map = battle_map

    def next_turn(self, active_unit):
        active_unit.start_turn()
        # Выбираем действие с наибольшим уровнем угрозы,
        # которое можем применить.
        decision = choose_action(active_unit, self.map)
        active_unit.take_action(
            action_index=decision.action_id,
            target=decision.target,
            battle_map=self.map,
            new_position=decision.chosen_position,
        )
        active_unit.end_turn()
