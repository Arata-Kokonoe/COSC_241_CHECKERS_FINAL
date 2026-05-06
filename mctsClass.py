import math, random
from node import Node
from draughts import Board, Move, WHITE, BLACK
import os
from functools import partial
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import time

class mctsClass():
    #numIterations controls how many times we run the full MCTS loop
    #explorationParameter controls how aggressively MCTS balances exploration vs. exploitation
    #simIterations controls how many simulations are done to evaluate each node
    def __init__(self, numIterations, explorationParameter, simIterations):
        self.numIterations = numIterations
        self.explorationParameter = explorationParameter
        self.simIterations = simIterations
        self.executor = ThreadPoolExecutor(max_workers=os.cpu_count())

    def search(self, board, numIterations=None, explorationParameter=None, simIterations=None):
        root = Node(board)
        rootPlayer = board.turn

        if len(root.untriedMoves) == 1:
            return root.untriedMoves[0]

        if numIterations:
            self.numIterations = numIterations
        if explorationParameter:
            self.explorationParameter = explorationParameter
        if simIterations:
            self.simIterations = simIterations

        for i in range(self.numIterations):
            t = time.perf_counter()
            # 1: Selection
            nodeToExpand = root
            while (not nodeToExpand.state.is_over()) and (len(nodeToExpand.untriedMoves) == 0):
                nodeToExpand = self.getBestChild(nodeToExpand, self.explorationParameter)
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
            value = self.simulation(nodeToEvaluate, self.simIterations, rootPlayer)
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

    def getBestChild(self, node, explorationParameter):
        for child in node.children:
            if child.numVisits == 0: return child
        childrenValues = {}
        logVisits = math.log(node.numVisits)
        for child in node.children:
            childrenValues[child] = self.UCB(child, logVisits, explorationParameter)
        return max(childrenValues, key=childrenValues.get)

    def UCB(self, node, logParentVisits, explorationParameter):
        UCB = node.value + (explorationParameter * math.sqrt(logParentVisits / node.numVisits))
        return UCB

    #uses epsilon-greedy policy to choose between random move or heuristically chosen move
    def fastRollout(self, board, rootPlayer):
        while not board.is_over():
            moves = board.legal_moves()
            #epsilon-greedy
            if random.random() < 0.2: #can replace 0.2 with higher value for more randomness
                nextMove = random.choice(moves)
            else:
                nextMove = self.fastHeuristic(board, moves, rootPlayer)
            board.push(nextMove)
        if board.winner() == rootPlayer: return 1
        elif board.winner() != rootPlayer and board.winner() is not None: return -1
        else: return 0

    #chooses random moves
    def randRollout(self, board, rootPlayer):
        while not board.is_over():
            moves = board.legal_moves()
            nextMove = random.choice(moves)
            board.push(nextMove)
        if board.winner() == rootPlayer: return 1
        elif board.winner() != rootPlayer and board.winner() is not None: return -1
        else: return 0

    def simulation(self, node, simIterations, rootPlayer):
        print(f"Running {simIterations} simulations using {os.cpu_count()} CPU cores...")
        results = list(self.executor.map(self.fastRollout, [node.state.copy() for _ in range(simIterations)], [rootPlayer] * simIterations))
        value = sum(results) / simIterations
        print(f"Average simulation value: {value}")
        return value
    
    #def simulation(self, node, simIterations, rootPlayer):
        #total = 0
        #board = node.state
        #for _ in range(simIterations):
        #    total += self.randRollout(board.copy(), rootPlayer)
        #return total / simIterations

    #scores each move based on how many capturable pieces you are left with after the move
    def fastHeuristic(self, state, moves, player):
        best_score = float('-inf')
        best_moves = []
        
        for move in moves:
            score = -self.countCapturablePieces(move)

            #can add more weights here to change score
            
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
        
        return random.choice(best_moves)

    def countCapturablePieces(self, move):
        return len(move.captures)
