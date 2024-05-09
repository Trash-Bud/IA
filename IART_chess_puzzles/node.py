from time import sleep
from chess_piece import ChessPiece
from position import Position
from itertools import combinations


def combine(arr, s):
    return list(combinations(arr, s))


class Node:
    def __init__(self, snake):
        self.snake = snake

    def print(self):
        print("Snake: ")
        for pos in self.snake:
            print(pos, end=", ")
        print("")

    def __eq__(self, __o: object) -> bool:
        if len(self.snake) != len(__o.snake):
            return False
        for i in range(len(self.snake)):
            if self.snake[i] != __o.snake[i]:
                return False
        return True

    def calculate_snake_heuristic(self, board, chess_pieces):
        attacking_pieces = {}
        for i in chess_pieces:
            attacking_pieces[i.textRepresentation] = 0
        for pos in self.snake:
            for piece in board[pos.x][pos.y].getAttackingPieces():
                attacking_pieces[piece.textRepresentation] += 1

        combinations = combine(attacking_pieces.keys(), 2)
        final_result = 0
        for combination in combinations:
            final_result += abs(attacking_pieces[combination[0]] -
                                attacking_pieces[combination[1]])
        return final_result

    def get_node_sucessors(self, board_size, board):
        successors = []

        sucessor_generation = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for suc in sucessor_generation:
            suc_x = self.snake[-1].x + suc[0]
            suc_y = self.snake[-1].y + suc[1]
            suc_pos = Position(suc_x, suc_y)
            if suc_x >= 0 and suc_x < board_size and suc_y >= 0 and suc_y < board_size and suc_pos not in self.snake and self.not_adjacent_to_snake(suc_pos) and type(board[suc_pos.x][suc_pos.y]) != ChessPiece:
                new_snake = self.snake + [suc_pos]
                successor = Node(new_snake)
                successors.append(successor)
        return successors

    def not_adjacent_to_snake(self, new_pos):
        # at the time of putting a square, check that it has no more than one diagonal adjacent already on the snake
        # if he does have, then its not a valid snake!

        new_pos_adjacents = [
            Position(new_pos.x - 1, new_pos.y), Position(new_pos.x +
                                                         1, new_pos.y), Position(new_pos.x, new_pos.y - 1),
            Position(new_pos.x, new_pos.y + 1)]

        new_pos_diagonals = [
            Position(new_pos.x - 1, new_pos.y - 1), Position(new_pos.x +
                                                             1, new_pos.y - 1), Position(new_pos.x + 1, new_pos.y + 1),
            Position(new_pos.x - 1, new_pos.y + 1)]
        num_of_adjacents = 0
        for neighbour in new_pos_diagonals:
            if neighbour in self.snake:
                num_of_adjacents += 1
        if num_of_adjacents > 1:
            return False

        num_of_adjacents = 0
        for neighbour in new_pos_adjacents:
            if neighbour in self.snake:
                num_of_adjacents += 1
        if num_of_adjacents != 1:
            return False
        return True
