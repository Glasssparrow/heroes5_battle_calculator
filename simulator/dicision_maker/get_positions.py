from ..battle_map.get_distance import get_distance

class AttackPositions:

    def __init__(self, action_index, action):
        self.positions = []
        self.action_name = action.name
        self.action_index = action_index  # position in unit's actions list.
        self.action_threat_lvl = action.threat

    def add_coord(self, x, y):
        self.positions.append((x, y))


def get_melee_attack_positions(the_unit, battle_map):
    attack_positions = []
    available_cells = battle_map.get_available_cells(the_unit)
    enemy_units = []
    for unit in battle_map.units:
        if unit.color != the_unit.color:
            enemy_units.append(unit)
    attack_positions_coords = []
    for (x, y), length, path in available_cells:
        for enemy in enemy_units:
            if get_distance(
                    coord1=(x, y),
                    is_big1=the_unit.big,
                    coord2=(enemy.coord[0], enemy.coord[1]),
                    is_big2=enemy.big,
            ) == 1:
                attack_positions_coords.append((x, y))
    for action_index, action in enumerate(the_unit.actions):
        attack_position = AttackPositions(
            action_index=action_index,
            action=action,
        )
        attack_positions.append(attack_position)
        for x, y in attack_positions_coords:
            attack_position.add_coord(x, y)


def get_range_attack_positions(unit, battle_map):
    attack_positions = []
