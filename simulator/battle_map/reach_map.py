

class ReachMap:

    def __init__(self, unit, length, height):
        # Карта в героях 10х12
        self.threat_for_big = []
        self.threat_for_small = []
        self.map_length = length
        self.map_height = height
        self.enemy_big = False
        melee_threat = 0
        for action in unit.actions:
            if action.range == 1 and action.threat > melee_threat:
                melee_threat = action.threat
        threat_dict = {}
        for action in unit.actions:
            if (
                action.range not in threat_dict.keys() or
                threat_dict[action.range] < action.threat
            ):
                threat_dict[action.range] = action.threat
        for x in range(height):
            for y in range(length):
                self.threat_for_big.append(0)
                self.threat_for_small.append(0)

    def _set_threat(self, coord, threat):
        pass

    def _increase_threat(self, coord, threat):
        pass

    def __getitem__(self, coord):
        # Возвращает величину угрозы для выбранной клетки
        x, y = coord[0], coord[1]
        if self.enemy_big:
            return self.threat_for_big[x + y * self.map_length]
        else:
            return self.threat_for_small[x + y * self.map_length]
