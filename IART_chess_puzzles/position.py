from __future__ import annotations


class Position:
    def __init__(self, X: int, Y: int):
        self.x = X
        self.y = Y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, x: int):
        self.x = x

    def setY(self, y: int):
        self.y = y

    def __str__(self) -> str:
        return '({self.x}, {self.y})'.format(self=self)

    def __eq__(self, other_pos: object) -> bool:
        if isinstance(other_pos, self.__class__):
            return self.x == other_pos.x and self.y == other_pos.y
        return False

    def get_manhattan_distance_between(self, point_b):
        return abs(self.x - point_b.x) + abs(self.y - point_b.y)
