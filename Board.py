from constants import *

class Board:
    def __init__(self, board_width, board_height):
        self.board = [[0] * board_width for _ in xrange(board_height)]

    def clear_lines(self):
        for i in xrange(BOARD_HEIGHT):
            need_to_clear = True
            for j in xrange(BOARD_WIDTH):
                if self.board[i][j] == 0:
                    need_to_clear = False
            if need_to_clear:
                del self.board[i]
                new_array = [0 for _ in xrange(BOARD_WIDTH)]
                self.board.insert(0, new_array)

    def draw_block_on_board(self, tetris_piece):
        block_row = len(tetris_piece.shapeArr)
        block_col = len(tetris_piece.shapeArr[0])
        for j in xrange(block_row):
            for i in xrange(block_col):
                if tetris_piece.shapeArr[j][i] != 0:
                    self.board[tetris_piece.y + j][tetris_piece.x + i] = tetris_piece.color

    def valid_position(self, tetris_piece, x, y):
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
                    if self.board[next_y][next_x] != 0:
                        return False
        return True

    def check_block_collision(self, tetris_piece):
        block_row = len(tetris_piece.shapeArr)
        block_col = len(tetris_piece.shapeArr[0])
        for j in xrange(block_row):
            for i in xrange(block_col):
                if not self.valid_position(tetris_piece, 0, 1):
                    return True
        return False


