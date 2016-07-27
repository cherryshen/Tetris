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

moving_left = False
moving_right = False
moving_down = False
moving_up = False

def create_board():
    return [[0] * BOARD_WIDTH for _ in xrange(BOARD_HEIGHT)]

# def create_piece(x, y):
#     return x, y, BOX_LENGTH, BOX_LENGTH

board = create_board()
start_x = BOARD_WIDTH / 2
start_y = 1
current_x = start_x
current_y = start_y

# currentPiece = create_piece(BOARD_WIDTH / 2, 1)

current_block = current_x, current_y
viewerSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def box_to_window_rect(x, y):
    x = BOX_LENGTH * x + BORDER_WIDTH
    y = BOX_LENGTH * y + BORDER_HEIGHT
    return x, y, BOX_LENGTH, BOX_LENGTH

def draw_board(board):
    for i in xrange(BOARD_HEIGHT):
        for j in xrange(BOARD_WIDTH):
            if board[i][j] != 0:
                viewerSurface.fill(board[i][j], box_to_window_rect(j, i))

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
            current_y += 1
    if current_x > 0:
        if moving_left:
            current_x -= 1
    if current_x < BOARD_WIDTH - 1:
        if moving_right:
            current_x += 1
    if current_y > 0:
        if moving_up:
            current_y -= 1

    viewerSurface.fill((0, 0, 0))
    viewerSurface.fill(GREEN, box_to_window_rect(current_x, current_y))
    draw_board(board)

    pygame.display.update()

    clock.tick(10)
