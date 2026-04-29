from draughts import Board, Move, WHITE, BLACK
#Create a game
board = Board(variant="english", fen="startpos")

#Make a move
#move = Move(board, steps_move=[34, 30])
#board.push(move)

# Multi-capture
board2 = Board(fen="W:WK40:B19,29")
board2.push(Move(board2, pdn_move='40x14'))

#Get a visual representation of the board as SVG
from draughts import svg
svg.create_svg(Board(fen="B:W16,19,33,34,47,K4:B17,25,26"))

#Get a visual representation of the board in the terminal
print(board)

moves = board.legal_moves()
print(moves)