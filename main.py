from draughts import Board
from mcts import MCTS

board = Board(variant="english", fen="startpos")
move = MCTS(board, numIterations=10, explorationParameter=1.4, simIterations=5)
print(f"MCTS returned move: {move}")
print(f"Is move legal? {move in board.legal_moves()}")