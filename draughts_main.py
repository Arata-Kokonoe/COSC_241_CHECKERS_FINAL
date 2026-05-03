import math, random
from draughts import Board, Move, WHITE, BLACK
from draughts.core.board_searcher import BoardSearcher

class opponent:
    def __init__(self, color = None)
        self.color = color
    
    def get_move(self, board):
        return best_move(board)

    def best_move(self, board)
        actions = board.legal_moves
        nextStates = []
        for move in board.legalMoves():
            newBoard = board.copy()
            newBoard.push(move)
            nextStates.append(newBoard)

        for opState in nextStates:
            
        


# This is the main draughts file. This is where we have the two agents
# who will play against each other or something like that.

