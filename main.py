from draughts import Board, svg
from mcts import MCTS
from mctsClass import mctsClass

board = Board(variant="english", fen="startpos")
move_count = 0
mcts = mctsClass(board)
while not board.is_over():
    #tests mcts function version (original)
    #move = MCTS(board, numIterations=10, explorationParameter=1.4, simIterations=5)
    
    #tests mcts class version
    move = mcts.search(numIterations=10, explorationParameter=1.4, simIterations=5)

    #move = mcts.search(numIterations=10, explorationParameter=1.4, simIterations=30)
    
    board.push(move)
    move_count += 1
    print(f"Move {move_count}: {move.pdn_move}")
    print(board)  # Display board as text
print(f"Game ended. Winner: {board.winner()}")