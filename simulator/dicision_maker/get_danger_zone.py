from ..simulator_keywords import MELEE_ACTION


class DangerZone:

    def __init__(self, height, length):
        self.height = height
        self.length = length
        self.data = []
        self.danger_map = []
        for x in range(length):
            self.data.append([False]*height)
            self.danger_map.append([0]*height)
        self.danger = 0

    def set_skill_danger_level(self, danger_level):
        # Устанавливает новый уровень угрозы и обновляет
        # карту угрозы.
        self.danger = danger_level
        self.create_danger_map()

    def create_danger_map(self):
        # Заполняет карту угрозы
        for x in range(self.length):
            for y in range(self.height):
                if self.data[x][y]:
                    self.danger_map[x][y] = self.danger
                else:
                    self.danger_map[x][y] = 0

    def get_danger(self, x_coord, y_coord):
        return self.danger_map[x_coord][y_coord]

    def __getitem__(self, item):
        # Если в рамках карты, возвращаем в зоне угрозы ли ячейка.
        if item[0] < self.length and item[1] < self.height:
            return self.data[item[0]][item[1]]
        else:  # Если ячейка вне зоны карты, то и вне зоны угрозы.
            return False

    def __setitem__(self, key, value):
        if not isinstance(value, bool):
            raise Exception(
                f"Допустимо лишь True/False, получено - {value}"
            )
        # Если ячейка в пределах карты, записываем значение,
        # иначе ничего не делаем.
        if key[0] < self.length and key[1] < self.height:
            self.data[key[0]][key[1]] = value

    def __delitem__(self, key):
        if key[0] < self.length and key[1] < self.height:
            self.data[key[0]][key[1]] = False

    def __iter__(self):
        self.for_iterator = []
        for y in range(self.height):
            for x in range(self.length):
                self.for_iterator.append((x, y,))
        self.iteration = -1
        return self

    def __next__(self):
        self.iteration += 1
        if self.iteration < len(self.for_iterator):
            return (
                self.for_iterator[self.iteration][0],  # x_coord
                self.for_iterator[self.iteration][1],  # y_coord
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
    danger_tmp.set_skill_danger_level(danger)  # Устанавливаем уровень угрозы.
    # Заполняем danger_tmp
    for coord, length, path in available_cells:
        attack_area = get_attack_area(
            x=coord[0], y=coord[1],
            big=unit.big,
        )
        for cell in attack_area:
            danger_tmp[cell[0], cell[1]] = True
    return danger_tmp


def get_danger_zone(the_unit, battle_map):
    melee_danger = get_melee_danger_zone(battle_map, the_unit)

