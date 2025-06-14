_nfa_state_counter = 0

class state:
    def __init__(self):
        self.transitions = {} 
        self.id = None 

    def add_transition(self, symbol, next_state):
        if symbol not in self.transitions:
            self.transitions[symbol] = set()
        self.transitions[symbol].add(next_state)

    def __hash__(self):
        return hash(self.id) if self.id is not None else super().__hash__()
    
    def __eq__(self,other):
        return isinstance(other,state) and self.id == other.id
    
    def __repr__(self):
        return f"state({self.id if self.id is not None else id(self)})"

class nfa:
    initial, accept = None, None

    def __init__(self, initial, accept):
        self.initial, self.accept = initial, accept
        self._states = set()
        self._collect_states()
        self._assign_stable_ids()
    
    def get_states(self):
        return self._states
    
    def _collect_states(self):
        visited = set()
        stack = [self.initial]
        while stack:
            s = stack.pop()
            if s not in visited:
                visited.add(s)
                self._states.add(s)
                for symbol, next_states in s.transitions.items():
                    for next_s in next_states:
                        stack.append(next_s)
    
    def _assign_stable_ids(self):
        global _nfa_state_counter
        sorted_states = sorted(list(self._states),key=lambda s:id(s))

        for s in sorted_states:
            if s.id is None:
                s.id = _nfa_state_counter
                _nfa_state_counter+=1

def compile(regex):
    nfaStack = []
    for c in regex:
        if c == '*':
            nfa1 = nfaStack.pop()
            initial, accept = state(), state()
            
            initial.add_transition(None, nfa1.initial) 
            initial.add_transition(None, accept) 
            
            nfa1.accept.add_transition(None, nfa1.initial) 
            nfa1.accept.add_transition(None, accept)
            
            nfaStack.append(nfa(initial, accept))
        
        elif c == '.': #concantenation
            nfa2 = nfaStack.pop()
            nfa1 = nfaStack.pop()
            nfa1.accept.add_transition(None, nfa2.initial)
            nfaStack.append(nfa(nfa1.initial, nfa2.accept))
        
        elif c == '+':
            nfa1 = nfaStack.pop()
            initial, accept = state(), state()
            
            initial.add_transition(None, nfa1.initial) 
            
            nfa1.accept.add_transition(None, nfa1.initial)
            nfa1.accept.add_transition(None, accept)
            
            nfaStack.append(nfa(initial, accept))
        
        elif c == '?': 
            nfa1 = nfaStack.pop()
            initial, accept = state(), state()
            
            initial.add_transition(None, nfa1.initial) 
            initial.add_transition(None, accept)  
            
            nfa1.accept.add_transition(None, accept) 
            
            nfaStack.append(nfa(initial, accept))
        
        elif c == '|':
            nfa2 = nfaStack.pop()
            nfa1 = nfaStack.pop()
            initial, accept = state(), state()
            
            initial.add_transition(None, nfa1.initial)
            initial.add_transition(None, nfa2.initial) 
            
            nfa1.accept.add_transition(None, accept)
            nfa2.accept.add_transition(None, accept)
            
            nfaStack.append(nfa(initial, accept))
        
        else:
            initial = state()
            accept = state()
            initial.add_transition(c, accept)
            nfaStack.append(nfa(initial, accept))
    
    return nfaStack.pop()