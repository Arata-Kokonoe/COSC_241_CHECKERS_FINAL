import math, random
from node import Node
from draughts import Board, Move, WHITE, BLACK
from copy import deepcopy

class mctsClass():
    def __init__(self, board):
        rootBoard = board.copy()
        self.root = Node(rootBoard)
        self.rootPlayer = rootBoard.turn      

    def search(self, numIterations, explorationParameter, simIterations):

        for i in range(numIterations):
            # 1: Selection
            nodeToExpand = self.root
            while (not nodeToExpand.state.is_over()) and (len(nodeToExpand.untriedMoves) == 0):
                nodeToExpand = self.getBestChild(nodeToExpand, explorationParameter)
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
            value = self.simulation(nodeToEvaluate, simIterations, self.rootPlayer)
            # 4: Backpropagate
            nodeToEvaluate.value = value
            nodeToEvaluate.numVisits += 1
            currNode = nodeToEvaluate
            while currNode.parent:
                currNode = currNode.parent
                currNode.value += value
                currNode.numVisits += 1
        # get the best action from root after numIterations
        bestChild = max(self.root.children, key=lambda child: child.value)
        newBoard = self.root.state.copy()
        newBoard.push(bestChild.move)
        self.root = Node(newBoard)
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

    def fastRollout(self, board, rootPlayer):
        currState = board.copy()
        while not currState.is_over():
            moves = currState.legal_moves()
            #epsilon-greedy
            if random.random() < 0.2: #can replace 0.2 with higher value for more randomness
                nextMove = random.choice(moves)
            else:
                nextMove = self.rolloutHeuristic(currState, moves, rootPlayer)
            currState.push(nextMove)
        if currState.winner() == rootPlayer: return 1
        elif currState.winner() != rootPlayer and currState.winner() is not None: return -1
        else: return 0

    def randRollout(self, board, rootPlayer):
        currState = board.copy()
        while not currState.is_over():
            moves = currState.legal_moves()
            nextMove = random.choice(moves)
            currState.push(nextMove)
        if currState.winner() == rootPlayer: return 1
        elif currState.winner() != rootPlayer and currState.winner() is not None: return -1
        else: return 0

    def simulation(self, node, simIterations, rootPlayer):
        totalValue = 0
        for i in range(simIterations):
            totalValue += self.fastRollout(node.state, rootPlayer)
        return totalValue / simIterations

    def rolloutHeuristic(self, state, moves, player):
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