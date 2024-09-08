from ..simulator_keywords import MELEE_ACTION


class DangerZone:

    def __init__(self, height, length):
        self.height = height
        self.length = length
        self.danger_map = []
        for x in range(length):
            self.danger_map.append([0]*height)

    def __iter__(self):
        self.coord_for_iterator = []
        for y in range(self.height):
            for x in range(self.length):
                self.coord_for_iterator.append((x, y,))
        self.iteration = -1
        return self

    def __next__(self):
        self.iteration += 1
        if self.iteration < len(self.coord_for_iterator):
            return (
                self.coord_for_iterator[self.iteration][0],  # x_coord
                self.coord_for_iterator[self.iteration][1],  # y_coord
            )
        else:
            raise StopIteration


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
    danger_tmp = DangerZone(
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
    # Заполняем danger_tmp
    for coord, length, path in available_cells:
        attack_area = get_attack_area(
            x=coord[0], y=coord[1],
            big=unit.big,
        )
    return danger_tmp


def get_danger_zone(the_unit, battle_map):
    melee_danger = get_melee_danger_zone(battle_map, the_unit)
