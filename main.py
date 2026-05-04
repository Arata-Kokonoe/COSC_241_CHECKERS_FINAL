from time import time

from draughts import Board, svg
from mcts import MCTS
from mctsClass import mctsClass

def main():
    board = Board(variant="english", fen="startpos")
    move_count = 0
    mcts = mctsClass(board)
    while not board.is_over():
        #tests mcts function version (original)
        t1 = time()
        move = MCTS(board, numIterations=30, explorationParameter=1.4, simIterations=50)
        t2 = time()
        print(f"MCTS Move Time: {t2-t1:.2f}s")
        #tests mcts class version
        # t1 = time()
        # move = mcts.search(numIterations=10, explorationParameter=1.4, simIterations=10)
        # t2 = time()
        # print(f"MCTS Move Time: {t2-t1:.2f}s")
        board.push(move)
        move_count += 1
        print(f"Move {move_count}: {move.pdn_move}")
        print(board)  # Display board as text
    print(f"Game ended. Winner: {board.winner()}")

if __name__ == "__main__":
    main()