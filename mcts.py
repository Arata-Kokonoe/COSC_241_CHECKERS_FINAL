import math, random
from draughts import Board, Move, WHITE, BLACK
from copy import deepcopy

starting_board = Board(variant="english", fen="startpos")

BOARD_SIZE = starting_board.width

#returns 1 if white won, 2 if black won, 0 if none
def check_winner_state(board):
    if board.winner() == WHITE: return 1
    elif board.winner() == BLACK: return 2
    else: return None

def available_actions(board):
    return board.legal_moves()