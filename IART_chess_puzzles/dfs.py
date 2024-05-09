from node import Node
from solver import Solver


class DFSNode(Node):
    def __init__(self, snake):
        super().__init__(snake)


class DFSSolver(Solver):
    def __init__(self, initial_pos, final_pos, board_size, board, chess_pieces) -> None:
        super().__init__(initial_pos, final_pos, board_size, board, chess_pieces)

    def DFSUtil(self, node, visited, visited_nodes_num):
        visited.append(node)

        node_successors = node.get_node_sucessors(
            self.board_size, self.matrix)

        for neighbour in node_successors:
            if neighbour not in visited:
                visited_nodes_num += 1

                if neighbour.snake[-1] == self.final_pos and neighbour.calculate_snake_heuristic(self.matrix, self.chess_pieces) == 0:
                    print("num_of_visited nodes: ", len(visited))
                    return neighbour.snake

                result = self.DFSUtil(neighbour, visited, visited_nodes_num)
                if result != None:
                    return result

    def solve(self):

        visited = []
        visited_nodes_num = 0
        node = DFSNode([self.initial_pos])
        return self.DFSUtil(node, visited, visited_nodes_num)
