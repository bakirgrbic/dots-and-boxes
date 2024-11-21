from random import randrange
import pygame

from dots_and_boxes.game import DotsAndBoxesGame



def random_move(game: DotsAndBoxesGame):
    size = len(game.legal_moves)
    if size == 0:
        return False
    line = list(game.legal_moves)[randrange(size)]
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

def draw_board(game: DotsAndBoxesGame, screen):
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

if __name__ == "__main__":
    game = DotsAndBoxes()
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