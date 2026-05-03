import math, random
from node import Node
from draughts import Board, Move, WHITE, BLACK
from copy import deepcopy

#starting_board = Board(variant="english", fen="startpos")

#BOARD_SIZE = starting_board.width

#returns 1 if white won, 2 if black won, 0 if none
def check_winner_state(board):
    if board.winner() == WHITE: return 1
    elif board.winner() == BLACK: return 2
    else: return None

def available_actions(board):
    return board.legal_moves()

def MCTS(board, numIterations, explorationParameter, simIterations):
    root = Node(board)
    # for move in board.legalMoves():
    #     newBoard = board.create_new_board_from_move(move)
    #     nextStates.append(newBoard)
    # for state in nextStates: 
    #     root.children.add(Node(nextStates))
    for i in range(numIterations):
        # 1: Selection
        nodeToExpand = root
        while (not nodeToExpand.state.is_over()) and (len(nodeToExpand.untriedMoves) == 0):
            nodeToExpand = getBestChild(nodeToExpand, explorationParameter)
        # 2: Expansion
        move = nodeToExpand.untriedMoves.pop()
        newBoard = nodeToExpand.state.create_new_board_from_move(move)
        nodeToEvaluate = Node(newBoard, nodeToExpand, None, move)
        nodeToExpand.children.add(nodeToEvaluate)
        # 3: Simulate
        value = simulation(nodeToEvaluate, simIterations)
        # 4: Backpropagate
        nodeToEvaluate.value = value
        nodeToEvaluate.numVisits += 1
        currNode = nodeToEvaluate
        while currNode.parent:
            currNode = nodeToEvaluate.parent
            currNode.value = value
            currNode.numVisits += 1
    # get the best action from root after numIterations
    bestChild = max(root.children, key=lambda child: child.value)
    return bestChild.move

def getBestChild(node, explorationParameter):
    for child in node.children:
        if child.numVisits == 0: return child
    childrenValues = {}
    for child in node.children:
        childrenValues[child] = UCB(child, explorationParameter)
    return max(childrenValues, key=childrenValues.get)

def UCB(node, explorationParameter):
    UCB = node.value + (explorationParameter * math.sqrt(math.log(node.parent.numVisits) / node.numVisits))
    return UCB

def fastRollout(board):
    currState = board
    while not currState.is_over():
        moves = currState.legal_moves()
        nextMove = random.choice(moves)	# should be changed maybe? Use heuristic policy instead of random
        currState = currState.create_new_board_from_move(nextMove)
    # CHANGE CHANGE CHANGE (how do we tell the agent/opponent is playing for black or white?)
    if currState.winner() == WHITE: return 1
    elif currState.winner() == BLACK: return -1
    else: return 0

def simulation(node, simIterations):
    totalValue = 0
    for i in range(simIterations):
        totalValue += fastRollout(node.state)
    return totalValue / simIterations