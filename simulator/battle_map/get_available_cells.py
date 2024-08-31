from ..simulator_keywords import MELEE_ACTION


class BlockableDangerZones:

    def __init__(self, length, height, data):
        self._length = length
        self._height = height
        self._blockable_danger = data
        for x in range(length):
            self._blockable_danger.append([0] * height)

    def __getitem__(self, item):
        return self._blockable_danger[item[0]][item[1]]

    def __setitem__(self, key, value):
        if not isinstance(value, (float, int)):
            raise Exception(
                f"Допустимо лишь float/int, получено - {value}"
            )
        if 0 <= key[0] < self._length and 0 <= key[1] < self._height:
            self._blockable_danger[key[0]][key[1]] = value

    def __delitem__(self, key):
        self._blockable_danger[key[0]][key[1]] = 0


class DangerZones:

    def __init__(self, length, height, unit_in_danger):
        # TO DO
        # Добавить слои. Каждый противник в отдельный слой.
        # Формирование итоговой карты опасности методом
        # с учетом размера юнита и способности блокировать стрельбу.
        # Или может вообще переписать всё? Не нравится мне получившийся код.
        self.length = length
        self.height = height
        self._danger = []
        self._blockable_danger = []
        self._blockable_danger_instance = BlockableDangerZones(
            length=length,
            height=height,
            data=self._blockable_danger,
        )
        for x in range(length):
            self._danger.append([0] * height)
            self._blockable_danger.append([0] * height)

    @property
    def blockable(self):
        return self._blockable_danger_instance

    def __getitem__(self, item):
        return self._danger[item[0]][item[1]]

    def __setitem__(self, key, value):
        if not isinstance(value, (float, int)):
            raise Exception(
                f"Допустимо лишь float/int, получено - {value}"
            )
        if 0 <= key[0] < self.length and 0 <= key[1] < self.height:
            self._danger[key[0]][key[1]] = value

    def __delitem__(self, key):
        self._danger[key[0]][key[1]] = 0


class DangerZoneInProgress:

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


def get_available_cells(pathfinder_big, pathfinder_small, unit):
    x, y = unit.coord[0], unit.coord[1]
    # Возвращает экземпляр класса Path
    if unit.big:
        return pathfinder_big(x, y, unit.speed)
    else:
        return pathfinder_small(x, y, unit.speed)


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
    danger_tmp = DangerZoneInProgress(
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


def add_tmp_melee_danger_zone_into_danger_zone(
        danger_zone, danger_zone_tmp
):
    danger_zone_tmp.create_danger_map()
    for x, y in danger_zone_tmp:
        pass


def get_danger_zone(battle_map, the_unit):
    result = DangerZones(
        height=battle_map.map_height,
        length=battle_map.map_length,
        unit_in_danger=the_unit,
    )
    for side_color, unit_ids_list in battle_map.sides.items():
        if side_color == the_unit.color:
            continue
        for unit_id in unit_ids_list:
            unit = battle_map.units[unit_id]
            danger_tmp = get_melee_danger_zone(battle_map, unit)
            add_tmp_melee_danger_zone_into_danger_zone(
                danger_zone=result,
                danger_zone_tmp=danger_tmp,
            )
    return result
