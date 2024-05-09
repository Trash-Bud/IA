
import pygame
from dfs import DFSSolver
from bfs import BFSSolver
from pygame_utils import Drawer
from game_levels import easy_game_board_init, hard_game_board_init, generate_board_from_file
from a_star import AStarSolver
from position import Position
import time

WINDOW_WIDTH = 450
WINDOW_HEIGHT = 600


class Game_State:
    def __init__(self, game) -> None:
        self.game = game
        self.drawer = Drawer(WINDOW_WIDTH, WINDOW_HEIGHT)

    def draw(self):
        pass

    def execute(self):
        pass


class Win_State(Game_State):
    def __init__(self, game) -> None:
        super().__init__(game)

    def draw(self):
        return self.drawer.draw_win_screen()

    def execute(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    new_state = Initial_State(self.game)
                    new_state.draw()
                    self.game.change_state(new_state)


class Lose_State(Game_State):
    def __init__(self, game) -> None:
        super().__init__(game)

    def draw(self):
        return self.drawer.draw_lose_screen()

    def execute(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    new_state = Initial_State(self.game)
                    new_state.draw()
                    self.game.change_state(new_state)


class Initial_State(Game_State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.custom_filename = 'custom_puzzle.txt'

    def draw(self):
        return self.drawer.draw_initial_menu()

    def execute(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    new_state = Puzzle_State(
                        self.game, easy_game_board_init())
                    new_state.draw()
                    self.game.change_state(new_state)

                elif event.key == pygame.K_2:
                    new_state = Puzzle_State(
                        self.game, hard_game_board_init())
                    new_state.draw()
                    self.game.change_state(new_state)
                elif event.key == pygame.K_3:
                    new_state = Puzzle_State(
                        self.game, generate_board_from_file(self.custom_filename))
                    new_state.draw()
                    self.game.change_state(new_state)


class Game:
    def __init__(self) -> None:
        self.game_state = Initial_State(self)
        self.run = True

    def change_state(self, new_state):
        self.game_state = new_state

    def play(self):
        self.game_state.draw()
        while self.game_state.execute() != -1:
            pass
        pygame.quit()


class Puzzle_State(Game_State):
    def __init__(self, game, board) -> None:
        super().__init__(game)
        self.board = board
        self.initial_point = Position(self.board.size - 1, 0)
        self.final_point = Position(0, self.board.size - 1)

    def draw(self):
        return self.drawer.draw_board(self.board)

    def check_player_solution(self, player_solution):

        self.board.executePieceMovements()
        a_star_solver = AStarSolver(
            self.initial_point, self.final_point, self.board.size, self.board.matrix, self.board.chess_pieces, "inequalities")

        solution_nodes = a_star_solver.solve()

        if len(player_solution) != len(solution_nodes):
            return False
        for i in range(len(player_solution)):

            if solution_nodes[i] != player_solution[i]:
                return False
        return True

    def execute(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                square_clicked = self.drawer.process_mouse_press(
                    mouse_pos, self.board.size)
                if square_clicked != None:
                    player_solution = self.board.process_square_clicked(
                        square_clicked)
                    self.drawer.draw_board(self.board)
                    if player_solution != None:
                        time.sleep(0.5)
                        if self.check_player_solution(player_solution):

                            game_win_state = Win_State(self.game)
                            game_win_state.draw()
                            self.game.change_state(game_win_state)
                        else:

                            game_lose_state = Lose_State(self.game)
                            game_lose_state.draw()
                            self.game.change_state(game_lose_state)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    new_state = Initial_State(
                        self.game)
                    new_state.draw()
                    self.game.change_state(new_state)
                if event.key == pygame.K_1:
                    print("Pressed 1")
                    bfs_solver = BFSSolver(
                        self.initial_point, self.final_point, self.board.size, self.board.matrix, self.board.chess_pieces)
                    start = time.time()
                    solution_nodes = bfs_solver.solve()
                    end = time.time()
                    if solution_nodes == None:
                        print("THIS PUZZLE HAS NO SOLUTION!")
                    else:
                        self.drawer.draw_solution(self.board, solution_nodes)
                        print("BFS Time: ", end-start, "seconds")
                        time.sleep(1)
                if event.key == pygame.K_2:
                    print("Pressed 2")
                    dfs_solver = DFSSolver(
                        self.initial_point, self.final_point, self.board.size, self.board.matrix, self.board.chess_pieces)
                    start = time.time()
                    solution_nodes = dfs_solver.solve()
                    end = time.time()
                    if solution_nodes == None:
                        print("THIS PUZZLE HAS NO SOLUTION!")
                    else:
                        self.drawer.draw_solution(self.board, solution_nodes)
                        print("DFS Time: ", end-start, "seconds")
                        time.sleep(1)
                if event.key == pygame.K_3:
                    print("Pressed 3")
                    a_star_solver = AStarSolver(
                        self.initial_point, self.final_point, self.board.size, self.board.matrix, self.board.chess_pieces, "shortest_distance")
                    start = time.time()
                    solution_nodes = a_star_solver.solve()
                    end = time.time()
                    if solution_nodes == None:
                        print("THIS PUZZLE HAS NO SOLUTION!")
                    else:
                        self.drawer.draw_solution(self.board, solution_nodes)
                        print("AStar shortest dist Time: ",
                              end-start, "seconds")
                        time.sleep(1)
                if event.key == pygame.K_4:
                    print("Pressed 4")
                    a_star_solver = AStarSolver(
                        self.initial_point, self.final_point, self.board.size, self.board.matrix, self.board.chess_pieces, "inequalities")
                    start = time.time()
                    solution_nodes = a_star_solver.solve()
                    end = time.time()
                    if solution_nodes == None:
                        print("THIS PUZZLE HAS NO SOLUTION!")
                    else:
                        self.drawer.draw_solution(self.board, solution_nodes)
                        print("AStar inequalities Time: ",
                              end-start, "seconds")
                        time.sleep(1)
