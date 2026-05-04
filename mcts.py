import math, random
from time import time
from tracemalloc import start
from node import Node
from draughts import Board, Move, WHITE, BLACK
from copy import deepcopy
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
import os

def MCTS(board, numIterations, explorationParameter, simIterations):
    root = Node(board)
    rootPlayer = board.turn
    # print(f"Starting MCTS with root player: {'White' if rootPlayer == WHITE else 'Black'}")
    if len(root.untriedMoves) == 1:
        return root.untriedMoves[0]
    for i in range(numIterations):
        # 1: Selection
        nodeToExpand = root
        while (not nodeToExpand.state.is_over()) and (len(nodeToExpand.untriedMoves) == 0):
            nodeToExpand = getBestChild(nodeToExpand, explorationParameter)
        # 2: Expansion
        if nodeToExpand.untriedMoves:
            move = nodeToExpand.untriedMoves.pop()
            newBoard = nodeToExpand.state.copy()
            newBoard.push(move)
            nodeToEvaluate = Node(newBoard, nodeToExpand, move=move)
            nodeToExpand.children.append(nodeToEvaluate)
        else:
            nodeToEvaluate = nodeToExpand
        # 3: Simulate
        value = simulation(nodeToEvaluate, simIterations, rootPlayer)
        # 4: Backpropagate
        nodeToEvaluate.value = value
        nodeToEvaluate.numVisits += 1
        currNode = nodeToEvaluate
        while currNode.parent:
            currNode = currNode.parent
            currNode.value += value
            currNode.numVisits += 1
    # get the best action from root after numIterations
    bestChild = max(root.children, key=lambda child: child.value)
    return bestChild.move

def getBestChild(node, explorationParameter):
    for child in node.children:
        if child.numVisits == 0: return child
    childrenValues = {}
    logVisits = math.log(node.numVisits)
    for child in node.children:
        childrenValues[child] = UCB(child, logVisits, explorationParameter)
    return max(childrenValues, key=childrenValues.get)

def UCB(node, logParentVisits, explorationParameter):
    UCB = node.value + (explorationParameter * math.sqrt(logParentVisits / node.numVisits))
    return UCB

def fastRollout(board, rootPlayer):
    currState = board.copy()
    while not currState.is_over():
        moves = currState.legal_moves()
        #epsilon-greedy
        if random.random() < 0.2: #can replace 0.2 with higher value for more randomness
            nextMove = random.choice(moves)
        else:
            nextMove = rolloutHeuristic(currState, moves, rootPlayer)
        currState.push(nextMove)
    if currState.winner() == rootPlayer: return 1
    elif currState.winner() != rootPlayer and currState.winner() is not None: return -1
    else: return 0

def simulation(node, simIterations, rootPlayer):
    num_cpu = os.cpu_count()
    print(f"Running {simIterations} simulations using {num_cpu} CPU cores...")
    with ProcessPoolExecutor(max_workers=num_cpu) as executor:
        results = list(executor.map(fastRollout, [deepcopy(node.state)] * simIterations, [rootPlayer] * simIterations))
    value = sum(results) / simIterations
    print(f"Average simulation value: {value}")
    return value
#     # totalValue = 0
#     # for i in range(simIterations):
#     #     totalValue += fastRollout(node.state, rootPlayer)
#     # return totalValue / simIterations

def rolloutHeuristic(state, moves, player):
        best_score = float('-inf')
        best_moves = []
        
        for move in moves:
            score = -countCapturablePieces(move)

            #can add more weights here to change score
            
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
        
        return random.choice(best_moves)

def countCapturablePieces(move):
    return len(move.captures)