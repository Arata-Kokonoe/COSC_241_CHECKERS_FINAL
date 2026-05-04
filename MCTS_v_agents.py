from draughts import Board, WHITE, BLACK
from mcts import MCTS
from adv_agents import opponent, random_agent

board = Board(variant="english", fen="startpos")
agent1 = opponent(color = WHITE)
move_count = 0

while not board.is_over():
    if board.turn == WHITE:
        # move = agent1.get_move(board)
        move = MCTS(board, numIterations=2, explorationParameter=1.4, simIterations=5)
    else:
        # move = MCTS(board, numIterations=2, explorationParameter=1.4, simIterations=5)
        move = agent1.get_move(board)

    move_count += 1

    board.push(move)
    print(f"Move {move_count}: {move.pdn_move}")
    print(board)
    print()

print(board.winner())