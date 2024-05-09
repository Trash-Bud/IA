from time import sleep
from chess_piece import ChessPiece
from position import Position
from node import Node
from solver import Solver


class AStarNode(Node):
    def __init__(self, snake, h_value, g_value) -> None:
        super().__init__(snake)
        self.h = h_value
        self.g = g_value
        self.f = self.h + self.g

    def diff_between_bigger_heuristic(self, board, chess_pieces):
        attacking_pieces = {}
        for i in chess_pieces:
            attacking_pieces[i.textRepresentation] = 0
        for pos in self.snake:
            for piece in board[pos.x][pos.y].getAttackingPieces():
                attacking_pieces[piece.textRepresentation] += 1

        def squares_atk(piece):
            return attacking_pieces[piece.textRepresentation]
        chess_pieces.sort(key=squares_atk, reverse=True)
        most_atk = chess_pieces[0].textRepresentation
        second_most_atk = chess_pieces[1].textRepresentation
        return attacking_pieces[most_atk] - attacking_pieces[second_most_atk]

    def shortest_distance_heuristic(self, last_placed_pos, final_point):
        return last_placed_pos.get_manhattan_distance_between(final_point)

    def get_node_sucessors(self, board_size, board, chess_pieces, heuristic):
        successors = []
        final_point = Position(0, board_size - 1)
        sucessor_generation = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for suc in sucessor_generation:
            suc_x = self.snake[-1].x + suc[0]
            suc_y = self.snake[-1].y + suc[1]
            suc_pos = Position(suc_x, suc_y)
            if suc_x >= 0 and suc_x < board_size and suc_y >= 0 and suc_y < board_size and suc_pos not in self.snake and self.not_adjacent_to_snake(suc_pos) and type(board[suc_pos.x][suc_pos.y]) != ChessPiece:

                new_snake = self.snake + [suc_pos]
                sucessor = AStarNode(new_snake, 0, 0)
                if heuristic == "shortest_distance":
                    sucessor.h = sucessor.shortest_distance_heuristic(
                        suc_pos, final_point)
                elif heuristic == "inequalities":
                    sucessor.h = sucessor.diff_between_bigger_heuristic(
                        board, chess_pieces)
                sucessor.g = self.g + 1
                sucessor.f = sucessor.h + sucessor.g
                successors.append(sucessor)
        return successors


class AStarSolver(Solver):
    def __init__(self, initial_pos, final_pos, board_size, board, chess_pieces, heuristic) -> None:
        super().__init__(initial_pos, final_pos, board_size, board, chess_pieces)
        self.heuristic = heuristic

    def get_next_node_shortest(self, open_list):
        least_f_node = None
        least_f_value = 9999
        for node in open_list:
            if node.f < least_f_value:
                least_f_node = node
                least_f_value = node.f

        return least_f_node

    def get_next_node_ineq(self, open_list):
        least_f_node = None
        least_f_value = 9999
        longest_snake_size = -1
        for node in open_list:
            if len(node.snake) > longest_snake_size or (len(node.snake) == longest_snake_size and node.f <= least_f_value):
                least_f_node = node
                least_f_value = node.f
                longest_snake_size = len(node.snake)

        return least_f_node

    def solve(self):
        open_list = [AStarNode([self.initial_pos], 0, 0)]
        closed_list = []
        nodes_num = 0

        while len(open_list) > 0:
            node_to_explore = None
            if self.heuristic == "shortest_distance":
                node_to_explore = self.get_next_node_shortest(open_list)
            elif self.heuristic == "inequalities":
                node_to_explore = self.get_next_node_ineq(open_list)
            open_list.remove(node_to_explore)
            node_sucessors = node_to_explore.get_node_sucessors(
                self.board_size, self.matrix, self.chess_pieces, self.heuristic)
            nodes_num += 1
            for node in node_sucessors:

                if node.snake[-1] == self.final_pos and node.calculate_snake_heuristic(self.matrix, self.chess_pieces) == 0:
                    print("num_of_visited nodes: ", nodes_num)
                    return node.snake

                open_list.append(node)

            closed_list.append(node_to_explore)
