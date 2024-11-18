from random import randrange
import pygame

BOX_MASK = 0b0000_0000_1111_0000

PLAYER_ONE = 9
PLAYER_TWO = 8

LEFT = 3
TOP = 2
RIGHT = 1
BOTTOM = 0


class GameInfo:
    def __init__(self):
        self.score = [0, 0]
        self.turn = PLAYER_ONE
        self.finished = False

    def get_points(self):
        return self.score[PLAYER_ONE - self.turn]

    def get_player_one_points(self):
        return self.score[0]

    def get_player_two_points(self):
        return self.score[1]


class Board:
    def __init__(self):
        self.layout = [
            204, 68, 68, 68, 68, 68, 68, 68, 68, 102, 136, 0, 0, 0, 0, 0, 0, 0, 0, 34, 136, 0,
            0, 0, 0, 0, 0, 0, 0, 34, 136, 0, 0, 0, 0, 0, 0, 0, 0, 34, 136, 0, 0, 0, 0, 0, 0, 0,
            0, 34, 136, 0, 0, 0, 0, 0, 0, 0, 0, 34, 136, 0, 0, 0, 0, 0, 0, 0, 0, 34, 136, 0, 0,
            0, 0, 0, 0, 0, 0, 34, 136, 0, 0, 0, 0, 0, 0, 0, 0, 34, 153, 17, 17, 17, 17, 17, 17,
            17, 17, 51,
        ]

    def set_bit(self, row, column, shift):
        self.layout[row * 10 + column] |= 1 << shift

    def get_bit(self, row, column, shift):
        return (self.layout[row * 10 + column] & (1 << shift)) > 0


class Game:
    def __init__(self):
        self.board = Board()
        self.game_info = GameInfo()

    def get_line(self, num, player):
        box_num = num // 2
        row = box_num // 10
        col = box_num % 10
        side = num % 2
        return self.get_line_by(row, col, side, player)

    def get_line_by(self, row, column, side, player):
        return self.board.get_bit(row, column, side + (4 * (player % 2)))

    def set_line(self, num, player):
        box_num = num // 2
        row = box_num // 10
        col = box_num % 10
        side = num % 2
        self.set_line_by(row, col, side, player)

    def set_line_by(self, row, column, side, player):
        self.board.set_bit(row, column, side + (4 * (player % 2)))
        self.check_box(row, column, player)

        horizontal = 1 - side % 2
        h_amount = -1 * side + 1
        vertical = side % 2
        v_amount = -1 * side + 2

        extra_row = row + (horizontal * h_amount)
        extra_column = column + (vertical * v_amount)
        extra_side = side + (horizontal * (2 * h_amount) + (vertical * (2 * v_amount)))

        self.board.set_bit(extra_row, extra_column, extra_side + (4 * (player % 2)))
        self.check_box(extra_row, extra_column, player)

        self.game_info.turn = 9 - (self.game_info.turn % PLAYER_TWO)

    def check_box(self, row, column, player):
        if (self.board.layout[10 * row + column] & BOX_MASK) | \
           ((self.board.layout[10 * row + column] << 4) & BOX_MASK) == BOX_MASK:
            self.board.set_bit(row, column, player)
            self.game_info.score[PLAYER_ONE - player] += 1
            self.game_info.turn = 9 - (player % PLAYER_TWO)

    def is_possible(self, line):
        return not (self.get_line(line, PLAYER_ONE) or self.get_line(line, PLAYER_TWO))

def random_move(game: Game):
    lines = list(range(200))
    remaining_lines = list(filter(lambda line: game.is_possible(line), lines))
    size = len(remaining_lines)
    if size == 0:
        return False
    line = remaining_lines[randrange(size)]
    game.set_line(line, game.game_info.turn)
    return True


TOP_X, TOP_Y = 10, 10
WIDTH, HEIGHT = 380, 380
BAR_WIDTH, BAR_LEN = 5, HEIGHT // 10
OFFSET_X, OFFSET_Y = BAR_WIDTH / 2, BAR_WIDTH / 2
COLOR_GRID = [0, 0, 0]
COLOR_EMPTY = [255, 255, 255]
COLOR_PLAYER1 = [255, 0, 0]
COLOR_PLAYER2 = [0, 0, 255]

def draw_board(game: Game, screen):
    pygame.draw.rect(screen, COLOR_GRID, [TOP_X, TOP_Y, WIDTH, HEIGHT])

    for row in range(10):
        for col in range(10):
            x = col * BAR_LEN
            y = row * BAR_LEN 


            color = (
                COLOR_PLAYER1 if game.board.get_bit(row, col, 9) else
                COLOR_PLAYER2 if game.board.get_bit(row, col, 8) else
                [0, 0, 0] 
            )

            pygame.draw.rect(screen, color, [TOP_X + x, TOP_Y+ y, BAR_LEN, BAR_LEN])

            if row < 9:
                color = (
                    COLOR_PLAYER1 if game.board.get_bit(row, col, 4) else
                    COLOR_PLAYER2 if game.board.get_bit(row, col, 0) else
                    COLOR_EMPTY
                )
                edge_rect = [
                    TOP_X + x + BAR_WIDTH - OFFSET_X,
                    TOP_Y + y + BAR_LEN - OFFSET_Y,
                    BAR_LEN - BAR_WIDTH,
                    BAR_WIDTH
                ]
                pygame.draw.rect(screen, color, edge_rect)

            x = col * BAR_LEN + BAR_LEN

            if col < 9:
                color = (
                    COLOR_PLAYER1 if game.board.get_bit(row, col, 5) else
                    COLOR_PLAYER2 if game.board.get_bit(row, col, 1) else
                    COLOR_EMPTY
                )
                edge_rect = [
                    TOP_X + x - OFFSET_X,
                    TOP_Y + y + BAR_WIDTH - OFFSET_Y,
                    BAR_WIDTH,
                    BAR_LEN - BAR_WIDTH
                ] 
                pygame.draw.rect(screen, color, edge_rect)

def start_game():
    game = Game()
    pygame.init()
    pygame.display.set_caption('Dots & Boxes')
    screen = pygame.display.set_mode((400, 400))
    clock = pygame.time.Clock()
    running = True

    COLOR_BG = "white"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(COLOR_BG)

        draw_board(game, screen)

        pygame.display.flip()
        if not random_move(game):
            running = False
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    start_game()