from time import time

from draughts import Board, WHITE, BLACK
from mcts import MCTS
from mctsClass import mctsClass
from adv_agents import random_agent


def playVsRandom(numGames, colorForMCTS):
    whiteWins = blackWins = total = 0

    for i in range(numGames):
        board = Board(variant="english", fen="startpos")
        move_count = 0
        
        mcts = mctsClass(numIterations=30, explorationParameter=1.4, simIterations=7)
        randAgent = random_agent()
        
        t1 = time()

        if colorForMCTS is BLACK:
            while not board.is_over():
                #black moves first
                mctsMove = mcts.search(board)
                board.push(mctsMove)
                move_count += 1

                if board.is_over(): break;

                #white moves second
                randMove = randAgent.get_move(board)
                board.push(randMove)
                move_count += 1

        else:
            while not board.is_over():
                #black moves first
                randMove = randAgent.get_move(board)
                board.push(randMove)
                move_count += 1

                if board.is_over(): break;

                #white moves second
                mctsMove = mcts.search(board)
                board.push(mctsMove)
                move_count += 1

        print(f"Game ended. Winner: {board.winner()}")
        if board.winner() == WHITE: whiteWins += 1
        else: blackWins += 1

        t2 = time()
        print(f"Game Time: {t2-t1:.2f}s")
        total += (t2-t1)

    print(f"Total WHITE wins: {whiteWins}. Total BLACK wins: {blackWins}. Winrate: {whiteWins/(whiteWins+blackWins)}")
    print(f"Average Time Per Game: {total/numGames}.")

if __name__ == "__main__":
    playVsRandom(10, BLACK)
    playVsRandom(10, WHITE)