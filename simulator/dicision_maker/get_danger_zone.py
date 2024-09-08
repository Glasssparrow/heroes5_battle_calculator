from ..simulator_keywords import MELEE_ACTION


class DangerZone:

    def __init__(self, height, length):
        self.height = height
        self.length = length
        self.danger_map = []
        for x in range(length):
            self.danger_map.append([0] * height)

    def __getitem__(self, item):
        return self.danger_map[item[0]+self.length*item[1]]

    def __setitem__(self, key, value):
        if not isinstance(value, (float, int)):
            raise Exception(
                f"Допустимо лишь float/int, получено - {type(value)}"
            )
        if 0 <= key[0] < self.length and 0 <= key[1] < self.height:
            self.danger_map[key[0]+self.length*key[1]] = value

    def __delitem__(self, key):
        self.danger_map[key[0]+self.length*key[1]] = 0


class DangerMap:

    def __init__(self, height, length):
        self.height = height
        self.length = length
        self.melee_danger_map = []
        self.range_danger_map = []
        self.spells_danger_map = []

    def set_melee_danger_zone(self, range_danger_map):
        self.range_danger_map = range_danger_map

    def set_range_danger_zone(self, range_danger_map):
        self.range_danger_map = range_danger_map

    def set_spell_danger_zone(self, range_danger_map):
        self.range_danger_map = range_danger_map


def get_attack_area(x, y, big):
    attack_area = []
    if big:
        for dx, dy in [
            (0, 1), (1, 1), (1, 0), (1, -1),
            (0, -1), (-1, -1), (-1, 0), (-1, 1),
        ]:
            attack_area.append((x+dx, y+dy))
    else:
        for dx, dy in [
            (0, -1), (+1, -1,), (+2, -1),
            (+2, 0), (+2, +1), (+2, +2),
            (+1, +2), (0, +2), (-1, +2),
            (-1, +1), (-1, 0), (-1, -1)
        ]:
            attack_area.append((x + dx, y + dy))
    return attack_area


def get_melee_danger_zone(battle_map, unit):
    # Временная карта опасности.
    # Её мы и будем возвращать.
    melee_danger = DangerZone(
        height=battle_map.map_height,
        length=battle_map.map_length,
    )
    available_cells = battle_map.get_available_cells(unit)
    # Выбираем сильнейшую атаку ближнего боя
    danger = 0
    for action in unit.actions:
        if (
            action.type_of_action == MELEE_ACTION and
            action.threat > danger
        ):
            danger = action.threat
    if danger == 0:  # Если не нашли рукопашных атак, значит что-то не так.
        raise Exception(
            f"{unit.name} не найдено действие рукопашной атаки."
        )
    # Заполняем melee_danger
    for coord, length, path in available_cells:
        attack_area = get_attack_area(
            x=coord[0], y=coord[1],
            big=unit.big,
        )
        for (x, y) in attack_area:
            pass
    return melee_danger


def get_danger_zone(the_unit, battle_map):
    melee_danger = get_melee_danger_zone(battle_map, the_unit)
