from ..battle_map.battle_map import BattleMap
from ..dicision_maker.choose_action import choose_action
from ..dicision_maker.choose_target import choose_target


class TurnSimulator:

    def __init__(self, units: list, battle_map: BattleMap):
        self.units = units
        self.map = battle_map

    def next_turn(self, active_unit):
        active_unit.start_turn()
        # Выбираем действие с наибольшим уровнем угрозы,
        # которое можем применить.
        action_index = choose_action(active_unit, self.map)
        action = active_unit.actions[action_index]
        # Т.к. юнита только 2, а действия пока только ближнего боя,
        # цель это всегда второй юнит.
        # Ну или None, если действие это просто движение.
        target = choose_target(active_unit, action, self.map)
        if target:
            active_unit.take_action(action_index, target, self.map)
        active_unit.end_turn()
