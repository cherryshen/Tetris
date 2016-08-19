from tetris_piece import *
from random import randint


class Piece:
    def __init__(self, start_x, start_y):
        random_piece = randint(0, len(possible_pieces) - 1)
        random_rotation = randint(0, len(possible_pieces[random_piece]) - 1)
        random_color = randint(0, len(possible_colors) - 1)
        self.x = start_x/2
        self.y = start_y
        self.shapeArr = possible_pieces[random_piece][random_rotation]
        self.piece = random_piece
        self.rotation = random_rotation
        self.color = possible_colors[random_color]

    def copy(self, start_x, start_y):
        newPiece = Piece(start_x, start_y)
        newPiece.x = self.x
        newPiece.y = self.y
        newPiece.shapeArr = self.shapeArr
        newPiece.piece = self.piece
        newPiece.rotation = self.rotation
        newPiece.color = self.color
        return newPiece

    def rotate_block(self):
        curr_piece = self.piece
        total_rotations = len(possible_pieces[curr_piece])
        new_rotation = (self.rotation + 1) % total_rotations
        self.shapeArr = possible_pieces[curr_piece][new_rotation]
        self.rotation = new_rotation
