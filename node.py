class Node:
    
    #def __init__(self, state, parent, children, move):
    #    self.state = state
    #    self.parent = parent
    #    self.children = children
    #    self.numVisits = 0
    #    self.value = 0

    def __init__(self, board, parent = None, children = None):
        self.state = board
        self.parent = parent
        self.children = children
        self.numVisits = 0
        self.value = 0