import math, random
from node import Node
from draughts import Board, Move, WHITE, BLACK
from copy import deepcopy

#starting_board = Board(variant="english", fen="startpos")

#BOARD_SIZE = starting_board.width

#returns 1 if white won, 2 if black won, 0 if none
def check_winner_state(board):
    if board.winner() == WHITE: return 1
    elif board.winner() == BLACK: return 2
    else: return None

def available_actions(board):
    return board.legal_moves()

def MCTS(board, numIterations, explorationParameter, simIterations):
    root = Node(board)
    nextStates = []
    for move in board.legalMoves():
        newBoard = board.copy()
        newBoard.push(move)
        nextStates.append(newBoard)
    for state in nextStates: 
        root.children.add(Node(nextStates))
    for i in [0, numIterations]:
        # 1: Selection
        # 2: 
        # 3: Simulate
        # 4: Backpropagate
        break