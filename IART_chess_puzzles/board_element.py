from __future__ import annotations
import string


class BoardElement:
    def __init__(self, representation: string) -> None:
        self.textRepresentation = representation
        self.attackedBy = []

    def __str__(self) -> None:
        return self.textRepresentation

    def addAttackingPiece(self, chess_piece) -> None:
        if chess_piece not in self.attackedBy:
            self.attackedBy.append(chess_piece)

    def getAttackingPieces(self):
        return self.attackedBy


class EmptySquare(BoardElement):
    def __init__(self, representation=" ") -> None:
        super().__init__(representation)


class SolutionSquare(BoardElement):
    def __init__(self, representation="O") -> None:
        super().__init__(representation)


class ClickedSquare(BoardElement):
    def __init__(self, representation="1") -> None:
        super().__init__(representation)
