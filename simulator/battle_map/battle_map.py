from .get_distance import get_distance
from .dijkstra_on_grid import Pathfinder


class BattleMap:

    def __init__(self, map_height, map_length):
        # Лист юнитов, позиция в листе == id юнита.
        self.units = []
        # sides[side_color] = [same_color_unit_id_1, same_color_unit_id_2]
        self.sides = {}
        # pathfinders[side_color] = Pathfinder()
        self.pathfinders_small = {}
        self.pathfinders_big = {}
        # Упрощенные карты угрозы для юнитов.
        # id юнита это его позиция в листе.

        # Размеры карты
        self.map_height = map_height
        self.map_length = map_length

    def create_pathfinders(self):
        """
        Создание в экземпляре карт проходимости для всех сторон.
        """
        for side_name in self.sides.keys():
            self.pathfinders_big[side_name] = Pathfinder(
                self.map_height,
                self.map_length,
            )
            # Блокируем нижний и правый ряды т.к. большие существа
            # не могут на них встать (координата по левому верхней
            # левой ячейке)
            for x in range(self.map_length):
                self.pathfinders_big[side_name].block_cell(
                    x, self.map_height - 1
                )
            for y in range(self.map_height):
                self.pathfinders_big[side_name].block_cell(
                    self.map_length - 1, y
                )
            self.pathfinders_small[side_name] = Pathfinder(
                self.map_height,
                self.map_length,
            )
        for side_name, units in self.sides.items():
            # Помечаем ячейку занятой для своей фракции
            for number in units:
                unit = self.units[number]
                x, y = unit.coord[0], unit.coord[1]
                self.pathfinders_small[side_name].occupy_cell(x, y)
                self.pathfinders_big[side_name].occupy_cell(x, y)
            # Блокируем ячейку для чужих фракций
            for side in self.sides.keys():
                if side == side_name:
                    continue
                for number in units:
                    unit = self.units[number]
                    x, y = unit.coord[0], unit.coord[1]
                    self.pathfinders_small[side].block_cell(x, y)
                    self.pathfinders_big[side].block_4_cells(x, y)

    def add_unit(self, unit, x, y, color=None):
        if color:
            unit.color = color
        if unit.color not in self.sides.keys():
            self.sides[unit.color] = [len(self.units),]
        else:
            self.sides[unit.color].append(len(self.units))
        unit.coord = (x, y)
        unit.pos = unit.coord[0] + unit.coord[1] * 12
        unit.side = self.sides[unit.color]
        unit.id = len(self.units)
        self.units.append(unit)

    @staticmethod
    def move_unit(unit, x, y):
        distance = abs(x-unit.coord[0]) + abs(y-unit.coord[1])
        unit.coord = (x, y)
        unit.pos = unit.coord[0] + unit.coord[1] * 12
        unit.tiles_moved = distance

    @staticmethod
    def get_distance(coord1, coord2, is_big1, is_big2):
        return get_distance(coord1, coord2, is_big1, is_big2)

    @staticmethod
    def get_distance_between_units(unit1, unit2):
        return get_distance(
            unit1.coord, unit2.coord, unit1.big, unit2.big
        )
    
    def get_available_cells(self, unit):
        pathfinder_big = self.pathfinders_big[unit.color]
        pathfinder_small = self.pathfinders_small[unit.color]
        x, y = unit.coord[0], unit.coord[1]
        # Возвращает экземпляр класса Path
        if unit.big:
            return pathfinder_big(x, y, unit.speed)
        else:
            return pathfinder_small(x, y, unit.speed)

    def apply_auras(self, unit):
        pass

    def get_visualisation(self):
        visualisation = []
        for line in range(10):
            visualisation.append(["  .  "]*12)
        for unit in self.units:
            coord = unit.coord
            visualisation[coord[1]][coord[0]] = unit.color
            if unit.big:
                for x, y in [(0, 1), (1, 0), (1, 1)]:
                    visualisation[coord[1]+y][coord[0]+x] = unit.color
        picture = ""
        for line in reversed(visualisation):
            for x in line:
                picture += x[0:5]
            picture += "\n"
        return picture
