class nfa:
    initial, accept = None, None

    def __init__(self, initial, accept):
        self.initial, self.accept = initial, accept

    def get_states(self):
        visited = set()
        stack = [self.initial]
        while stack:
            state = stack.pop()
            if state not in visited:
                visited.add(state)
                if state.edge1:
                    stack.append(state.edge1)
                if state.edge2:
                    stack.append(state.edge2)
        return visited

class state:
    def __init__(self, label=None):
        self.label = label
        self.edge1 = None
        self.edge2 = None
        self.id = id(self)

def compile(regex):

    nfaStack = []

    for c in regex:
        if c == '*':
            nfa1 = nfaStack.pop()
            initial, accept = state(), state()
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 =  accept
            nfaStack.append(nfa(initial,accept))

        elif c == '.':
            nfa2 = nfaStack.pop()
            nfa1 = nfaStack.pop()
            nfa1.accept.edge1 = nfa2.initial
            nfaStack.append(nfa(nfa1.initial, nfa2.accept))

        elif c == '+':
            nfa1 = nfaStack.pop()
            accept, initial = state(), state()
            initial.edge1 = nfa1.initial
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
            nfaStack.append(nfa(initial,accept))

        elif c == '?':
            nfa1 = nfaStack.pop()
            initial, accept = state(), state()
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            nfa1.accept.edge1 = accept
            nfaStack.append(nfa(initial,accept))

        elif c == '|':
            nfa2 = nfaStack.pop()
            nfa1 = nfaStack.pop()
            accept, initial = state(), state()
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept
            nfaStack.append(nfa(initial, accept))

        else:
            accept = state()
            initial = state(label=c)
            initial.edge1 = accept
            nfaStack.append(nfa(initial,accept))

    return nfaStack.pop()


