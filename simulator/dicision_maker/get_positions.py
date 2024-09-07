

class AttackPositions:

    def __init__(self, action_index, action):
        self.positions = []
        self.action_name = action.name
        self.action_index = action_index  # position in unit's actions list.
        self.action_threat_lvl = action.threat


def get_melee_attack_positions(unit, battle_map):
    attack_positions = []
    available_cells = battle_map.get_available_cells(unit)
    for (x, y), length, path in available_cells:
        pass
    for action_index, action in enumerate(unit.actions):
        attack_positions.append(AttackPositions(
            action_index=action_index,
            action=action,
        ))


def get_range_attack_positions(unit, battle_map):
    attack_positions = []
