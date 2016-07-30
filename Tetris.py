import pygame, sys
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

BORDER_WIDTH = 3
BORDER_HEIGHT = 3
BOX_LENGTH = 20
BOARD_WIDTH = 10 # need 10 boxes
BOARD_HEIGHT = 20 # need 20 boxes
WINDOW_WIDTH = BOARD_WIDTH * BOX_LENGTH + BORDER_WIDTH * 2
WINDOW_HEIGHT = BOARD_HEIGHT * BOX_LENGTH + BORDER_HEIGHT * 2
RED = (255,   0,   0)
GREEN = (0,   255,   0)

SHAPE_ARR = "shape_array"

moving_left = False
moving_right = False
moving_down = False
moving_up = False

def create_board():
    return [[0] * BOARD_WIDTH for _ in xrange(BOARD_HEIGHT)]

def create_piece():
    return {"start_x": BOARD_WIDTH/2, "start_y": 1, SHAPE_ARR: [[0, 0, 1], [0, 1, 1], [0, 1, 0]]}

board = create_board()
start_x = BOARD_WIDTH / 2
start_y = 1
current_x = start_x
current_y = start_y

current_block = create_piece()
viewerSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

block_row = len(current_block[SHAPE_ARR])
block_col = len(current_block[SHAPE_ARR][0])

def box_to_window_rect(x, y):
    x = BOX_LENGTH * x + BORDER_WIDTH
    y = BOX_LENGTH * y + BORDER_HEIGHT
    return x, y, BOX_LENGTH, BOX_LENGTH

def draw_board(board):
    for i in xrange(BOARD_HEIGHT):
        for j in xrange(BOARD_WIDTH):
            if board[i][j] != 0:
                viewerSurface.fill(board[i][j], box_to_window_rect(j, i))

def draw_piece(current_block):
    for j in xrange(block_row):
        for i in xrange(block_col):
            if current_block[SHAPE_ARR][j][i] == 1:
                viewerSurface.fill(GREEN, box_to_window_rect(current_block["start_x"]+i, current_block["start_y"] + j))

def valid_position(current_block, x, y):
    for j in xrange(block_row):
        for i in xrange(block_col):
            if current_block["start_x"] + i + x < -1 or current_block["start_x"] + i + x > BOARD_WIDTH - 1:
                return False
            if current_block["start_y"] + j + y > BOARD_HEIGHT - 1:
                return False
            if board[current_block["start_y"] + j][current_block["start_x"] + i] != 0:
                return False
    return True

def draw_block_on_board(current_block, board):
    for j in xrange(block_row):
        for i in xrange(block_col):
            if current_block[SHAPE_ARR][j][i] != 0:
                board[current_block["start_y"]+j][current_block["start_x"]+i] = RED

def check_block_collision(current_block):
    for j in xrange(block_row):
        for i in xrange(block_col):
            if j == block_row - 1:
                if not valid_position(current_block, 0, 1):
                    return True
    return False


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                moving_down = event.type == pygame.KEYDOWN
            if event.key == pygame.K_UP:
                moving_up = event.type == pygame.KEYDOWN
            if event.key == pygame.K_LEFT:
                moving_left = event.type == pygame.KEYDOWN
            if event.key == pygame.K_RIGHT:
                moving_right = event.type == pygame.KEYDOWN

    if current_y < BOARD_HEIGHT - 1:
        if moving_down:
            if valid_position(current_block, 0, 1):
                current_block["start_y"] += 1
    if current_x > 0:
        if moving_left:
            if valid_position(current_block, -1, 0):
                current_block["start_x"] -= 1
    if current_x < BOARD_WIDTH - 1:
        if moving_right:
            if valid_position(current_block, 1, 0):
                current_block["start_x"] += 1
    if current_y > 0:
        if moving_up:
            if valid_position(current_block, 0, -1):
                current_block["start_y"] -= 1

    if check_block_collision(current_block):
        draw_block_on_board(current_block, board)
        current_block = create_piece()

    viewerSurface.fill((0, 0, 0))
    draw_piece(current_block)
    draw_board(board)

    pygame.display.update()

    clock.tick(10)
