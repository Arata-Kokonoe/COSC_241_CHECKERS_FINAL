from draughts import Board, svg
from mcts import MCTS

board = Board(variant="english", fen="startpos")
move_count = 0
while not board.is_over():
    move = MCTS(board, numIterations=10, explorationParameter=1.4, simIterations=5)
    board.push(move)
    move_count += 1
    print(f"Move {move_count}: {move.pdn_move}")
    print(board)  # Display board as text
print(f"Game ended. Winner: {board.winner()}")