import pygame, sys
from pygame.locals import *
from constants import *
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
score = 0
level = 1
cleared_lines = 0
game_paused = False

def create_board():
    return [[0] * BOARD_WIDTH for _ in xrange(BOARD_HEIGHT)]

def rotate_block(tetris_piece):
    curr_piece = tetris_piece.piece
    total_rotations = len(possible_pieces[curr_piece])
    new_rotation = (tetris_piece.rotation + 1) % total_rotations
    tetris_piece.shapeArr = possible_pieces[curr_piece][new_rotation]
    tetris_piece.rotation = new_rotation

def level_and_score():
    global cleared_lines
    score = cleared_lines
    level = cleared_lines % 10
    return score, level

board = create_board()

current_block = Piece(BOARD_WIDTH, 1)
viewerSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(TITLE)
game_window_width = viewerSurface.get_width() / 2
game_window_height = viewerSurface.get_height() / 2

def box_to_window_rect(x, y):
    x = BOX_LENGTH * x + BORDER_WIDTH
    y = BOX_LENGTH * y + BORDER_HEIGHT
    return x, y, BOX_LENGTH, BOX_LENGTH


def draw_board(board):
    for i in xrange(BOARD_HEIGHT):
        for j in xrange(BOARD_WIDTH):
            if board[i][j] != 0:
                viewerSurface.fill(board[i][j], box_to_window_rect(j, i))
                pygame.draw.rect(viewerSurface, WHITE, Rect(box_to_window_rect(j, i)), 1)


def draw_piece(tetris_piece):
    block_row = len(tetris_piece.shapeArr)
    block_col = len(tetris_piece.shapeArr[0])
    for j in xrange(block_row):
        for i in xrange(block_col):
            if tetris_piece.shapeArr[j][i] == 1:
                viewerSurface.fill(tetris_piece.color, box_to_window_rect(tetris_piece.x+i, tetris_piece.y + j))
                pygame.draw.rect(viewerSurface, WHITE, Rect(box_to_window_rect(tetris_piece.x+i, tetris_piece.y + j)), 1)


def clear_lines():
    global cleared_lines
    for i in xrange(BOARD_HEIGHT):
        need_to_clear = True
        for j in xrange(BOARD_WIDTH):
            if board[i][j] == 0:
                need_to_clear = False
        if need_to_clear:
            cleared_lines += 1
            del board[i]
            new_array = [0 for _ in xrange(BOARD_WIDTH)]
            board.insert(0, new_array)


def draw_block_on_board(tetris_piece, board):
    block_row = len(tetris_piece.shapeArr)
    block_col = len(tetris_piece.shapeArr[0])
    for j in xrange(block_row):
        for i in xrange(block_col):
            if tetris_piece.shapeArr[j][i] != 0:
                board[tetris_piece.y+j][tetris_piece.x+i] = tetris_piece.color


def valid_position(tetris_piece, x, y):
    block_row = len(tetris_piece.shapeArr)
    block_col = len(tetris_piece.shapeArr[0])
    for j in xrange(block_row):
        for i in xrange(block_col):
            if tetris_piece.shapeArr[j][i] == 1:
                next_x = tetris_piece.x + i + x
                next_y = tetris_piece.y + j + y
                if next_x < 0 or next_x > BOARD_WIDTH - 1:
                    return False
                if next_y > BOARD_HEIGHT - 1:
                    return False
                if board[next_y][next_x] != 0:
                    return False
    return True


def check_block_collision(tetris_piece):
    block_row = len(tetris_piece.shapeArr)
    block_col = len(tetris_piece.shapeArr[0])
    for j in xrange(block_row):
        for i in xrange(block_col):
            if not valid_position(tetris_piece, 0, 1):
                return True
    return False

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

    if not game_paused:
        if is_fast_drop:
            while valid_position(current_block, 0, 1):
                current_block.y += 1
                last_falling_block_time = pygame.time.get_ticks()

        if current_block.y < BOARD_HEIGHT - 1:
            if moving_down:
                if valid_position(current_block, 0, 1):
                    current_block.y += 1
                    last_falling_block_time = pygame.time.get_ticks()

        if current_block.x >= 0:
            if moving_left:
                if valid_position(current_block, -1, 0):
                    current_block.x -= 1
                    last_falling_block_time = pygame.time.get_ticks()

        if current_block.x < BOARD_WIDTH - 1:
            if moving_right:
                if valid_position(current_block, 1, 0):
                    current_block.x += 1
                    last_falling_block_time = pygame.time.get_ticks()

        if pygame.time.get_ticks() - last_falling_block_time > FALLING_BLOCK_FREQUENCY:
            if valid_position(current_block, 0, 1):
                current_block.y += 1
                last_falling_block_time = pygame.time.get_ticks()

        if rotate:
            rotated_block = current_block.copy(BOARD_WIDTH/2, 1)
            rotate_block(rotated_block)
            if valid_position(rotated_block, 0, 0):
                current_block = rotated_block

        if check_block_collision(current_block):
            if not valid_position(current_block, 0, 0):
                game_over = True
            else:
                draw_block_on_board(current_block, board)
                is_fast_drop = False
                current_block = Piece(BOARD_WIDTH, 1)

    viewerSurface.fill((0, 0, 0))

    if valid_position(current_block, 0, 0):
        draw_piece(current_block)
    clear_lines()
    draw_board(board)

    if game_paused:
        viewerSurface.fill(WHITE)
        viewerSurface.blit(pause_text, [game_window_width - pause_text.get_rect().width / 2, game_window_height - \
                                        pause_text.get_rect().height / 2])

    if game_over:
        game_over_text = game_font.render(TEXT_GAME_OVER, True, BLACK)
        game_over_rect = game_over_text.get_rect()
        game_over_x = game_window_width - game_over_rect.width / 2
        game_over_y = game_window_height - game_over_rect.height / 2
        viewerSurface.blit(game_over_text, [game_over_x, game_over_y])

    pygame.display.update()

    clock.tick(10)