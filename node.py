class Node:
    def __init__(self, state, parent, children, move):
        self.state = state
        self.parent = parent
        self.children = children
        self.numVisits = 0
        self.value = 0