from draughts import Board, WHITE, BLACK
from mcts import MCTS
from adv_agents import opponent, random_agent
import time
from mctsClass import mctsClass

def play_games(games = 100):
    results = {WHITE: 0, BLACK: 0, "draw": 0}
    game_times = []
    
    with open("game_results.txt", "w") as f:
        f.write(f"Starting new tournament: {games} games\n")
        f.write("=" * 50 + "\n\n")
        f.flush()
    
    for i in range(games):
        start_time = time.time()

        print(f"Starting game {i + 1}")
        board = Board(variant="english", fen="startpos")
        numMoves = 0
        mctsShallow = mctsClass(numIterations=10, explorationParameter=1.4, simIterations=10)
        mctsDeep = mctsClass(numIterations=30, explorationParameter=1.4, simIterations=10)
        while not board.is_over():
            t1 = time.perf_counter()
            if board.turn == WHITE:
                move = mctsDeep.search(board)
            else:
                move = mctsShallow.search(board)
            t2 = time.perf_counter()
            print(f"Move {numMoves + 1}: {'White' if board.turn == WHITE else 'Black'} plays {move.pdn_move} (Time: {t2 - t1:.2f}s)")

            board.push(move)
            print(board)
            numMoves += 1
        winner = board.winner()

        end_time = time.time()
        duration = end_time - start_time
        game_times.append(duration)
        print(f"Round {i + 1} took {duration:.2f} seconds\n")

        if winner == WHITE:
            results[WHITE] += 1
            result_str = "WHITE"
        elif winner == BLACK:
            results[BLACK] += 1
            result_str = "BLACK"
        else:
            results["draw"] += 1
            result_str = "DRAW"
        
        # Write result to file immediately
        with open("game_results.txt", "a") as f:
            f.write(f"Game {i + 1}: {result_str} (Duration: {duration:.2f}s)\n")
            f.write(f"Current Record - White: {results[WHITE]}, Black: {results[BLACK]}, Draws: {results['draw']}\n")
            f.write("-" * 50 + "\n")
            f.flush()
    
    # Write final summary
    with open("game_results.txt", "a") as f:
        f.write("\n" + "=" * 50 + "\n")
        f.write(f"FINAL RESULTS after {games} games:\n")
        f.write(f"White Wins: {results[WHITE]}\n")
        f.write(f"Black Wins: {results[BLACK]}\n")
        f.write(f"Draws: {results['draw']}\n")
        f.write(f"Average game time: {sum(game_times)/len(game_times):.2f}s\n")
        f.flush()
    
    print("Results after", games, "games:")
    print(results)
    print()
    print(game_times)
    print("Results saved to game_results.txt")

play_games(100)