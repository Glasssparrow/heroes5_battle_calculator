

def get_distance(coord1, coord2, is_big1, is_big2):
    """Вернуть расстояние между двумя юнитами.

    coord1: Координаты первого юнита (x, y)
    coord2: Координаты второго юнита (x, y)
    is_big1: Является ли юнит1 большим (True/False)
    is_big2: Является ли юнит2 большим (True/False)
    :return Расстояние int
    Расстояние возвращается равным единице если возможна
    рукопашная атака.
    """
    if not is_big1 and not is_big2:
        x_distance = abs(coord1[0] - coord2[0])
        y_distance = abs(coord1[1] - coord2[1])
        if x_distance == y_distance == 1:
            return 1
        else:
            return x_distance+y_distance
    unit1_coord = {0: None, 1: None}
    unit2_coord = {0: None, 1: None}
    for axis in (0, 1):
        if coord1[axis] > coord2[axis]:
            unit1_coord[axis] = coord1[axis]
            if is_big2:
                unit2_coord[axis] = coord2[axis] + 1
            else:
                unit2_coord[axis] = coord2[axis]
        elif coord1[axis] < coord2[axis]:
            unit2_coord[axis] = coord2[axis]
            if is_big1:
                unit1_coord[axis] = coord1[axis] + 1
            else:
                unit1_coord[axis] = coord1[axis]
        else:
            unit1_coord[axis] = coord1[axis]
            unit2_coord[axis] = coord2[axis]
    x_distance = abs(unit1_coord[0] - unit2_coord[0])
    y_distance = abs(unit1_coord[1] - unit2_coord[1])
    if x_distance == y_distance == 1:
        return 1
    else:
        return x_distance + y_distance
