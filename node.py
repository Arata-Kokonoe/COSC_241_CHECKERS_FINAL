import math, random
from draughts import Board, Move, WHITE, BLACK
from copy import deepcopy

class Node:

    def __init__(self, board, parent = None, children = None, move = None, numVisits = 0, value = 0, untriedMoves = None):
        self.state = board
        self.parent = parent
        self.children = []
        self.move = move
        self.numVisits = numVisits
        self.value = value
        self.untriedMoves = board.legal_moves()