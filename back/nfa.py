# U nfa.py

class state:
    def __init__(self):
        self.transitions = {} # {'symbol': set_of_next_states, None: set_of_epsilon_next_states}
        self.id = id(self) # Jedinstveni ID za svako stanje

    def add_transition(self, symbol, next_state):
        if symbol not in self.transitions:
            self.transitions[symbol] = set()
        self.transitions[symbol].add(next_state)

class nfa:
    initial, accept = None, None

    def __init__(self, initial, accept):
        self.initial, self.accept = initial, accept
    
    def get_states(self):
        visited = set()
        stack = [self.initial]
        while stack:
            s = stack.pop()
            if s not in visited:
                visited.add(s)
                for symbol, next_states in s.transitions.items():
                    for next_s in next_states:
                        stack.append(next_s)
        return visited

def compile(regex):
    nfaStack = []
    for c in regex:
        if c == '*': # Kleene star
            nfa1 = nfaStack.pop()
            initial, accept = state(), state()
            
            initial.add_transition(None, nfa1.initial) # New_initial --e--> Old_initial
            initial.add_transition(None, accept)      # New_initial --e--> New_accept (0 ponavljanja)
            
            nfa1.accept.add_transition(None, nfa1.initial) # Old_accept --e--> Old_initial (ponavljanja)
            nfa1.accept.add_transition(None, accept)       # Old_accept --e--> New_accept
            
            nfaStack.append(nfa(initial, accept))
        
        elif c == '.': # Konkatenacija
            nfa2 = nfaStack.pop()
            nfa1 = nfaStack.pop()
            nfa1.accept.add_transition(None, nfa2.initial) # NFA1_accept --e--> NFA2_initial
            nfaStack.append(nfa(nfa1.initial, nfa2.accept))
        
        elif c == '+': # Kleene plus
            nfa1 = nfaStack.pop()
            initial, accept = state(), state()
            
            initial.add_transition(None, nfa1.initial) # New_initial --e--> Old_initial
            
            nfa1.accept.add_transition(None, nfa1.initial) # Old_accept --e--> Old_initial (ponavljanja)
            nfa1.accept.add_transition(None, accept)       # Old_accept --e--> New_accept
            
            nfaStack.append(nfa(initial, accept))
        
        elif c == '?': # Opcionalni operator
            nfa1 = nfaStack.pop()
            initial, accept = state(), state()
            
            initial.add_transition(None, nfa1.initial) # New_initial --e--> Old_initial
            initial.add_transition(None, accept)      # New_initial --e--> New_accept (0 ponavljanja)
            
            nfa1.accept.add_transition(None, accept)   # Old_accept --e--> New_accept
            
            nfaStack.append(nfa(initial, accept))
        
        elif c == '|': # Unija
            nfa2 = nfaStack.pop()
            nfa1 = nfaStack.pop()
            initial, accept = state(), state()
            
            initial.add_transition(None, nfa1.initial) # New_initial --e--> NFA1_initial
            initial.add_transition(None, nfa2.initial) # New_initial --e--> NFA2_initial
            
            nfa1.accept.add_transition(None, accept)   # NFA1_accept --e--> New_accept
            nfa2.accept.add_transition(None, accept)   # NFA2_accept --e--> New_accept
            
            nfaStack.append(nfa(initial, accept))
        
        else: # Literalni karakter
            initial = state()
            accept = state()
            initial.add_transition(c, accept) # Initial --c--> Accept
            nfaStack.append(nfa(initial, accept))
    
    return nfaStack.pop()