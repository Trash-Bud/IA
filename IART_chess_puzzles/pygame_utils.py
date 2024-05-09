
import pygame
import time
from a_star import AStarNode

WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
GRAY_COLOR = (192, 192, 192)
GREEN_COLOR = (0, 200, 0)
BLUE_COLOR = (0, 0, 255)
RED_COLOR = (255, 0, 0)
PURPLE_COLOR = (128, 0, 128)


def setup_pygame_window(window_width, window_height):
    pygame.init()
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Chess Puzzles")
    return window


class Drawer:
    def __init__(self, window_width, window_height) -> None:
        self.window = setup_pygame_window(window_width, window_height)
        self.window_width = window_width
        self.window_height = window_height
        self.show_attacked_squares = True
        self.gui_height = 0.25 * window_height
        self.puzzle_height = self.window_height - self.gui_height
        self.font_name = 'freesansbold.ttf'
        self.load_sprites()

    def toggle_attacked_squares(self):
        self.show_attacked_squares = not self.show_attacked_squares

    def process_mouse_press(self, mouse_pos, board_size):
        # find which square has been pressed
        if mouse_pos[1] > self.puzzle_height:
            return None
        rect_width = int(self.window_width / board_size)
        rect_height = int(self.puzzle_height / board_size)
        return (mouse_pos[1] // rect_height, mouse_pos[0] // rect_width)

    def load_sprites(self):
        king_sprite = pygame.image.load(
            "piece_sprites/king_sprite.png").convert_alpha()

        queen_sprite = pygame.image.load(
            "piece_sprites/queen_sprite.png").convert_alpha()

        rook_sprite = pygame.image.load(
            "piece_sprites/rook_sprite.png").convert_alpha()

        knight_sprite = pygame.image.load(
            "piece_sprites/knight_sprite.png").convert_alpha()

        bishop_sprite = pygame.image.load(
            "piece_sprites/bishop_sprite.png").convert_alpha()
        self.sprites = {"K": king_sprite,
                        "Q": queen_sprite,
                        "R": rook_sprite,
                        "k": knight_sprite,
                        "B": bishop_sprite}

    def draw_solution(self, board, solution_squares):
        rect_border_width = 2
        rect_width = int(self.window_width / board.size)
        rect_height = int(self.puzzle_height / board.size)
        for node_pos in solution_squares:
            upper_width = node_pos.y * rect_width
            upper_height = node_pos.x * rect_height
            pygame.draw.rect(self.window, BLUE_COLOR,
                             (upper_width, upper_height, rect_width, rect_height))
            pygame.draw.rect(self.window, BLACK_COLOR,
                             (upper_width, upper_height, rect_width, rect_height), rect_border_width)

        pygame.display.update()

    def draw_lose_screen(self):
        self.window.fill(GRAY_COLOR)

        font_text = pygame.font.Font(self.font_name, 50)
        text = font_text.render('YOU LOST :( ', True, WHITE_COLOR)
        textRect = text.get_rect()

        textRect.center = (self.window_width // 2,
                           self.window_height // 2)

        self.window.blit(text, textRect)

        font_text = pygame.font.Font(self.font_name, 25)
        text = font_text.render(
            'Press 1 to return to main screen', True, WHITE_COLOR)
        textRect = text.get_rect()

        textRect.center = (self.window_width // 2,
                           self.window_height // 2 + 100)

        self.window.blit(text, textRect)

        pygame.display.update()

    def draw_win_screen(self):
        self.window.fill(GRAY_COLOR)

        font_text = pygame.font.Font(self.font_name, 50)
        text = font_text.render('YOU WIN! ', True, WHITE_COLOR)
        textRect = text.get_rect()

        textRect.center = (self.window_width // 2,
                           self.window_height // 2)

        self.window.blit(text, textRect)

        font_text = pygame.font.Font(self.font_name, 25)
        text = font_text.render(
            'Press 1 to return to main screen', True, WHITE_COLOR)
        textRect = text.get_rect()

        textRect.center = (self.window_width // 2,
                           self.window_height // 2 + 100)

        self.window.blit(text, textRect)

        pygame.display.update()

    def draw_board(self, board):
        self.window.fill(WHITE_COLOR)
        rect_border_width = 2
        matrix = board.matrix
        rect_width = int(self.window_width / board.size)
        rect_height = int(self.puzzle_height / board.size)

        initial_y = board.size - 1
        initial_x = 0
        upper_width = initial_x * rect_width
        upper_height = initial_y * rect_height

        pygame.draw.rect(self.window, BLACK_COLOR,
                         (upper_height, upper_width, rect_width, rect_height))

        for x in range(board.size):
            upper_width = x * rect_width
            for y in range(board.size):
                upper_height = y * rect_height
                textRep = matrix[y][x].textRepresentation[0]
                if textRep == "1":
                    pygame.draw.rect(self.window, PURPLE_COLOR,
                                     (upper_width, upper_height, rect_width, rect_height))
                elif textRep != " ":
                    scaled_sprite = pygame.transform.scale(
                        self.sprites[textRep], (rect_width, rect_height))
                    self.window.blit(
                        scaled_sprite, (upper_width, upper_height, rect_width, rect_height))

                elif self.show_attacked_squares:
                    attackingPieces = matrix[y][x].attackedBy
                    if len(attackingPieces) > 0:
                        pygame.draw.rect(self.window, GRAY_COLOR,
                                         (upper_width, upper_height, rect_width, rect_height))

                pygame.draw.rect(self.window, BLACK_COLOR,
                                 (upper_width, upper_height, rect_width, rect_height), rect_border_width)

        # draw initial and final_squares

        # draw the GUI
        upper_width = 0
        upper_height = self.window_height - self.gui_height
        gui_width = self.window_width
        gui_height = self.gui_height
        pygame.draw.rect(self.window, GRAY_COLOR,
                         (upper_width, upper_height, gui_width, gui_height))

        font_options = pygame.font.Font(self.font_name, 20)
        text = font_options.render('0 - Back', True, WHITE_COLOR)
        textRect = text.get_rect()

        textRect.center = (self.window_width // 2 - self.window_width // 4,
                           (upper_height + 50))

        self.window.blit(text, textRect)

        text = font_options.render('1 - BFS', True, WHITE_COLOR)
        textRect = text.get_rect()

        textRect.center = (self.window_width // 2 + self.window_width // 4,
                           (upper_height + 50))

        self.window.blit(text, textRect)

        text = font_options.render('2 - DFS', True, WHITE_COLOR)
        textRect = text.get_rect()

        textRect.center = (self.window_width // 2 - self.window_width // 4,
                           (upper_height + 80))

        self.window.blit(text, textRect)

        text = font_options.render(
            '3 - A Star (shortest)', True, WHITE_COLOR)
        textRect = text.get_rect()

        textRect.center = (self.window_width // 2 + self.window_width // 4,
                           (upper_height + 80))

        self.window.blit(text, textRect)

        text = font_options.render(
            '4 - A Star (ineq)', True, WHITE_COLOR)
        textRect = text.get_rect()

        textRect.center = (self.window_width // 2 - self.window_width // 4,
                           (upper_height + 110))

        self.window.blit(text, textRect)
        pygame.display.update()

    def draw_initial_menu(self):
        self.window.fill(GRAY_COLOR)
        font_game_title = pygame.font.Font(self.font_name, 50)
        font_options = pygame.font.Font(self.font_name, 25)
        text = font_game_title.render('Chess Puzzles!', True, WHITE_COLOR)
        textRect = text.get_rect()

        textRect.center = (self.window_width // 2,
                           (self.window_height - 20) // 2)
        self.window.blit(text, textRect)

        text_easy_puzzle = font_options.render(
            '1 - Easy Puzzle', True, WHITE_COLOR)
        textRect = text_easy_puzzle.get_rect()

        textRect.center = (self.window_width // 2,
                           (self.window_height + 50) // 2)
        self.window.blit(text_easy_puzzle, textRect)

        text_hard_puzzle = font_options.render(
            '2 - Hard Puzzle', True, WHITE_COLOR)
        textRect = text_easy_puzzle.get_rect()

        textRect.center = (self.window_width // 2,
                           (self.window_height + 100) // 2)
        self.window.blit(text_hard_puzzle, textRect)

        text_custom_puzzle = font_options.render(
            '3 - Custom Puzzle', True, WHITE_COLOR)
        textRect = text_custom_puzzle.get_rect()

        textRect.center = (self.window_width // 2,
                           (self.window_height + 150) // 2)
        self.window.blit(text_custom_puzzle, textRect)
        pygame.display.update()
