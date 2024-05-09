from time import sleep
from chess_piece import ChessPiece
from position import Position
from itertools import combinations
from node import Node
from solver import Solver


class BFSNode(Node):
    def __init__(self, snake):
        super().__init__(snake)


class BFSSolver(Solver):
    def __init__(self, initial_pos, final_pos, board_size, board, chess_pieces) -> None:
        super().__init__(initial_pos, final_pos, board_size, board, chess_pieces)

    def solve(self):
        queue = [BFSNode([self.initial_pos])]
        visited = []
        visited_nodes_num = 0

        while len(queue) > 0:
            node = queue.pop(0)
            node_successors = node.get_node_sucessors(
                self.board_size, self.matrix)
            visited_nodes_num += 1

            for node in node_successors:
                if node.snake[-1] == self.final_pos and node.calculate_snake_heuristic(self.matrix, self.chess_pieces) == 0:
                    print("num_of_visited nodes: ", visited_nodes_num)
                    return node.snake
                queue.append(node)

            visited.append(node)
