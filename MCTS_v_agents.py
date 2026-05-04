from draughts import Board, WHITE, BLACK
from mcts import MCTS
from adv_agents import opponent, random_agent
import time
from mctsClass import mctsClass

# board = Board(variant="english", fen="startpos")
# agent1 = opponent(color = WHITE)
# move_count = 0


# while not board.is_over():
#     if board.turn == WHITE:
#         # move = agent1.get_move(board)
#         move = MCTS(board, numIterations=2, explorationParameter=1.4, simIterations=5)
#     else:
#         # move = MCTS(board, numIterations=2, explorationParameter=1.4, simIterations=5)
#         move = agent1.get_move(board)

#     move_count += 1

#     board.push(move)
#     print(f"Move {move_count}: {move.pdn_move}")
#     print(board)
#     print()

def play_games(games = 5):
    results = {WHITE: 0, BLACK: 0, "draw": 0}
    
    for i in range(games):
        start_time = time.time()

        print(f"Starting game {i + 1}")
        board = Board(variant="english", fen="startpos")
        agent1 = opponent(color = BLACK)
        numMoves = 0
        mcts = mctsClass(board)
        while not board.is_over() and numMoves < 75:
            if board.turn == WHITE:
                # move = agent1.get_move(board)
                move = mcts.search(numIterations=10, explorationParameter=1.4, simIterations=5)
            else:
                # move = mcts.search(numIterations=10, explorationParameter=1.4, simIterations=5)
                move = agent1.get_move(board)
            print(numMoves)
            print(move)
            board.push(move)
            print(board)
            numMoves += 1
        winner = board.winner()

        end_time = time.time()
        duration = end_time - start_time
        print(f"Round {i + 1} took {duration:.2f} seconds\n")

        if winner == WHITE:
            results[WHITE] += 1
        elif winner == BLACK:
            results[BLACK] += 1
        else:
            results["draw"] += 1    
    print("Results after", games, "games:")
    print(results)

play_games(5)
