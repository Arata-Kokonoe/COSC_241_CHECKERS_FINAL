import math, random
from draughts import Board, Move, WHITE, BLACK

#############
# The code below shows an opponent class that uses a greedy heuristic
# to determine which move it should take.
#############

class opponent:
    def __init__(self, color=None):
        self.color = color
    
    def get_move(self, board):
        return self.best_move(board)

    def best_move(self, board):
        best_move = None
        best_value = -float('inf')

        for move in board.legal_moves():
            newBoard = board.copy()
            newBoard.push(move)

            value = self.position_eval(newBoard)
            
            # Code below is subject to inclusion at a later date.
            # if self.color == BLACK:
            #     value = -value
            #     value += ((2 * len(newBoard.legal_moves())) * -1)
            # else:
            #     value += (2 * len(newBoard.legal_moves()))

            if value > best_value:
                best_value = value
                best_move = move
        
        return best_move

    def position_eval(self, board):
        hold = board.fen
        sections = hold.split(':')

        w_pieces = sections[1][1:].split(',')
        b_pieces = sections[2][1:].split(',')

        def score(pieces):
            val = 0
            for p in pieces:
                if p.startswith('K'):
                    val += 500
                else:
                    val += 100
            return val

        white_score = score(w_pieces)
        black_score = score(b_pieces)

        return white_score - black_score

###
# Below is a class that contains the code for an agent that plays randomly.
# What is does is self-explanatory, the bot chooses from available moves at random.
###

class random_agent:
    def get_move(self, board):
        moves = list(board.legal_moves())
        return random.choice(moves)
        


# This is the main draughts file. This is where we have the two agents
# who will play against each other or something like that.

