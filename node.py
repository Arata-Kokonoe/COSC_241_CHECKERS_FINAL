class Node:
    def __init__(state, parent, children, move):
        self.state = state
        self.parent = parent
        self.chidlren = children
        self.numVisits = 0
        self.value = 0