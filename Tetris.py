import pygame, sys, os
from pygame.locals import *
from Board import *
from Piece import *

pygame.init()

clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 45)
moving_left = False
moving_right = False
moving_down = False
rotate = False
last_falling_block_time = 0
is_fast_drop = False
game_over = False
cleared_lines = 0
game_paused = False
board = Board(BOARD_WIDTH, BOARD_HEIGHT)

dir_path = os.path.dirname(os.path.realpath(__file__))
music_filepath = dir_path + '/tetris_music.mid'
pygame.mixer.music.load(music_filepath)
pygame.mixer.music.play(-1, 0.0)

current_block = Piece(BOARD_WIDTH, 1)
viewerSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(TITLE)
game_window_width = viewerSurface.get_width()
game_window_height = viewerSurface.get_height()


def box_to_window_rect(x, y):
    x = BOX_LENGTH * x + BORDER_WIDTH
    y = BOX_LENGTH * y + BORDER_HEIGHT
    return x, y, BOX_LENGTH, BOX_LENGTH


def draw_board(board):
    for i in xrange(BOARD_HEIGHT):
        for j in xrange(BOARD_WIDTH):
            if board.board[i][j] != 0:
                viewerSurface.fill(board.board[i][j], box_to_window_rect(j, i))
                pygame.draw.rect(viewerSurface, WHITE, Rect(box_to_window_rect(j, i)), 1)


def draw_piece(tetris_piece):
    block_row = len(tetris_piece.shapeArr)
    block_col = len(tetris_piece.shapeArr[0])
    for j in xrange(block_row):
        for i in xrange(block_col):
            if tetris_piece.shapeArr[j][i] == 1:
                viewerSurface.fill(tetris_piece.color, box_to_window_rect(tetris_piece.x+i, tetris_piece.y + j))
                pygame.draw.rect(viewerSurface, WHITE, Rect(box_to_window_rect(tetris_piece.x+i, tetris_piece.y + j)), 1)

pause_text = game_font.render(TEXT_GAME_PAUSED, True, BLACK)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                moving_down = event.type == pygame.KEYDOWN
            if event.key == pygame.K_UP:
                rotate = event.type == pygame.KEYDOWN
            if event.key == pygame.K_LEFT:
                moving_left = event.type == pygame.KEYDOWN
            if event.key == pygame.K_RIGHT:
                moving_right = event.type == pygame.KEYDOWN
            if event.key == pygame.K_SPACE:
                is_fast_drop = event.type == pygame.KEYDOWN
            if event.key == pygame.K_p and event.type == pygame.KEYDOWN:
                game_paused = not game_paused

    if not game_paused and not game_over:
        if is_fast_drop:
            while board.valid_position(current_block, 0, 1):
                current_block.y += 1
                last_falling_block_time = pygame.time.get_ticks()

        if current_block.x >= 0:
            if moving_left:
                if board.valid_position(current_block, -1, 0):
                    current_block.x -= 1

        if current_block.x < BOARD_WIDTH - 1:
            if moving_right:
                if board.valid_position(current_block, 1, 0):
                    current_block.x += 1

        if rotate:
            rotated_block = current_block.copy(BOARD_WIDTH/2, 1)
            rotated_block.rotate_block()
            if board.valid_position(rotated_block, 0, 0):
                current_block = rotated_block
                rotate = False

        if not board.valid_position(current_block, 0, 0):
            game_over = True
        elif (is_fast_drop or moving_down or
              (pygame.time.get_ticks() - last_falling_block_time > FALLING_BLOCK_FREQUENCY)):
            last_falling_block_time = pygame.time.get_ticks()
            if board.valid_position(current_block, 0, 1):
                current_block.y += 1
            else:
                board.draw_block_on_board(current_block)
                is_fast_drop = False
                current_block = Piece(BOARD_WIDTH, 1)

    viewerSurface.fill((0, 0, 0))

    pygame.draw.rect(viewerSurface, GREEN, Rect(1, 2, BOARD_WIDTH*BOX_LENGTH + BORDER_WIDTH, \
                                                BOARD_HEIGHT*BOX_LENGTH + BORDER_WIDTH), BORDER_WIDTH)

    board.update_level()
    viewerSurface.blit(game_font.render("Score: "+str(board.score), True, BLUE), [game_window_width/2 + 50,
                                                                                  game_window_height/2.5])
    viewerSurface.blit(game_font.render("Level: " + str(board.level), True, TEAL), [game_window_width / 2 + 50,
                                                                                    game_window_height / 2])

    if board.valid_position(current_block, 0, 0):
        draw_piece(current_block)
        board.clear_lines()

    draw_board(board)

    if game_paused:
        viewerSurface.fill(WHITE)
        viewerSurface.blit(pause_text, [game_window_width - pause_text.get_rect().width / 2, game_window_height - \
                                        pause_text.get_rect().height / 2])

    if game_over:
        game_over_text = game_font.render(TEXT_GAME_OVER, True, WHITE)
        game_over_rect = game_over_text.get_rect()
        game_over_x = game_window_width/2 - game_over_rect.width / 2
        game_over_y = game_window_height/2 - game_over_rect.height / 2
        viewerSurface.blit(game_over_text, [game_over_x, game_over_y])

    pygame.display.update()

    clock.tick(10)