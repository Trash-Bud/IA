from turtle import pos
from board_element import BoardElement, ClickedSquare, EmptySquare
from chess_piece import ChessPiece
from a_star import AStarSolver, AStarNode
from position import Position


class Board:
    def __init__(self, size: int) -> None:
        self.size = size
        self.matrix = [[EmptySquare() for x in range(size)]
                       for x in range(size)]
        self.chess_pieces = []
        self.clicked_squares = [Position(self.size - 1, 0)]
        self.matrix[self.size - 1][0] = ClickedSquare()
        self.final_point = Position(0, self.size - 1)

    def add_piece(self, chess_piece: ChessPiece) -> None:
        x = chess_piece.position.getX()
        y = chess_piece.position.getY()
        for piece in self.chess_pieces:
            if (piece.position.x == x and piece.position.y == y):
                raise Exception("square already has another chess piece")
        self.chess_pieces.append(chess_piece)
        self.matrix[x][y] = chess_piece

    def executePieceMovements(self):
        for piece in self.chess_pieces:
            attackedPositions = piece.implementStrategy(self.size, self.matrix)
            for position in attackedPositions:
                x = position.getX()
                y = position.getY()
                self.matrix[x][y].addAttackingPiece(piece)

    def print(self) -> None:
        for i in self.matrix:
            print("[", end=" ")
            for j in i:
                print(j, end=" ")
            print("]")

    def print_all_attacked_squares(self):
        for i in range(self.size):
            for j in range(self.size):
                print("(", i, ",", j, ") - >",
                      self.matrix[i][j].getAttackingPieces())

    def valid_click(self, x, y):
        if type(self.matrix[x][y]) == ChessPiece:
            return False
        valid_dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dir in valid_dirs:
            if self.clicked_squares[-1].x - x == dir[0] and self.clicked_squares[-1].y - y == dir[1]:
                return True
        return False

    def process_square_clicked(self, square_clicked):
        x = square_clicked[0]
        y = square_clicked[1]
        if x == self.clicked_squares[-1].x and y == self.clicked_squares[-1].y:
            if len(self.clicked_squares) > 1:
                self.matrix[x][y] = EmptySquare()
                self.clicked_squares.pop()

        elif self.valid_click(x, y):
            self.matrix[x][y] = ClickedSquare()
            self.clicked_squares.append(Position(x, y))
            if x == self.final_point.x and y == self.final_point.y:
                return self.clicked_squares
