from __future__ import annotations
import string
from position import Position

from board_element import BoardElement


class ChessPiece(BoardElement):
    def __init__(self, position: Position, move_strategy, representation: string) -> None:
        self.move_strategy = move_strategy
        self.position = position
        BoardElement.__init__(self, representation)

    @property
    def getMoveStrategy(self):
        return self.move_strategy

    @property
    def getPosition(self) -> Position:
        return self.position

    def setMoveStrategy(self, move_strategy) -> None:
        self.move_strategy = move_strategy

    def implementStrategy(self, board_size, matrix):
        return self.move_strategy.execute(self.position, board_size, matrix)
