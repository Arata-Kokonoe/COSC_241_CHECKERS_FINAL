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

def play_games_b(games = 5):
    results = {WHITE: 0, BLACK: 0, "draw": 0}
    game_times = []
    
    for i in range(games):
        start_time = time.time()

        print(f"Starting game {i + 1}")
        board = Board(variant="english", fen="startpos")
        agent1 = opponent(color = BLACK)
        numMoves = 0
        mcts = mctsClass(numIterations=30, explorationParameter=1.4, simIterations=7)
        while not board.is_over() and numMoves < 75:
            if board.turn == WHITE:
                move = agent1.get_move(board)
                # move = MCTS(board, numIterations=30, explorationParameter=1.4, simIterations=7)
            else:
                move = mcts.search(board)
                # move = agent1.get_move(board)
            # print(numMoves)
            # print(move)
            board.push(move)
            # print(board)
            numMoves += 1
        winner = board.winner()

        end_time = time.time()
        duration = end_time - start_time
        game_times.append(duration)
        print(f"Round {i + 1} took {duration:.2f} seconds\n")

        hold = board.fen # This function gets the notation of the current board.
        sections = hold.split(':') # The FEN notation is split by colons.

        w_pieces = sections[1][1:].split(',') # refer to FEN notation to understand split here.
        b_pieces = sections[2][1:].split(',')

        white_score = score(w_pieces) # determine the value of all the white pieces.
        black_score = score(b_pieces) # determine the value of all the black pieces.
        
        if winner == None:
            if white_score > black_score:
                results[WHITE] += 1
            elif black_score > white_score:
                results[BLACK] += 1
            else:
                results["draw"] += 1 
            continue

        if winner == WHITE:
            results[WHITE] += 1
        elif winner == BLACK:
            results[BLACK] += 1
        else:
            results["draw"] += 1    
    print("Results after", games, "games:")
    print(results)
    print()
    print(game_times)

def play_games_w(games = 5):
    results = {WHITE: 0, BLACK: 0, "draw": 0}
    game_times = []
    
    for i in range(games):
        start_time = time.time()

        print(f"Starting game {i + 1}")
        board = Board(variant="english", fen="startpos")
        agent1 = opponent(color = WHITE)
        numMoves = 0
        mcts = mctsClass(numIterations=30, explorationParameter=1.4, simIterations=10)
        while not board.is_over() and numMoves < 75:
            if board.turn == WHITE:
                move = mcts.search(board)
            else:
                move = agent1.get_move(board)
            # print(numMoves)
            # print(move)
            board.push(move)
            # print(board)
            numMoves += 1
        winner = board.winner()

        end_time = time.time()
        duration = end_time - start_time
        game_times.append(duration)
        print(f"Round {i + 1} took {duration:.2f} seconds\n")

        hold = board.fen # This function gets the notation of the current board.
        sections = hold.split(':') # The FEN notation is split by colons.

        w_pieces = sections[1][1:].split(',') # refer to FEN notation to understand split here.
        b_pieces = sections[2][1:].split(',')

        white_score = score(w_pieces) # determine the value of all the white pieces.
        black_score = score(b_pieces) # determine the value of all the black pieces.
        
        if winner == None:
            if white_score > black_score:
                results[WHITE] += 1
            elif black_score > white_score:
                results[BLACK] += 1
            else:
                results["draw"] += 1 
            continue

        if winner == WHITE:
            results[WHITE] += 1
        elif winner == BLACK:
            results[BLACK] += 1
        else:
            results["draw"] += 1    
    print("Results after", games, "games:")
    print(results)
    print()
    print(game_times)

def score(pieces):
    val = 0
    for p in pieces:
        if p.startswith('K'):
            val += 200
        else:
            val += 100
    return val

play_games_w(25)
play_games_b(25)
