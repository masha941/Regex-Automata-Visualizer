class state:
    def __init__(self, nfa_states):
        self.nfa_states = frozenset(nfa_states)
        self.transitions = {}
        self.is_accept = False
        self.id = id(self)

    def __hash__(self):
        return hash(self.nfa_states)
    
    def __eq__(self, other):
        return isinstance(other, state) and self.nfa_states == other.nfa_states
    
    def __repr__(self):
        return f"state({sorted([s._temp_id for s in self.nfa_states])})"
    
class dfa:
    def __init__(self, initial_state, accept_states):
        self.initial = initial_state
        self.accept_states = accept_states
        self.states = set()
        self._collect_states()
        
    def _collect_states(self):
        visited = set()
        stack = [self.initial]

        while stack:
            curr = stack.pop()
            if curr not in visited:
                visited.add(curr) 
                self.states.add(curr)

                for next_state in curr.transitions.values():
                    stack.append(next_state) 

def epsilon_closure(states):
    closure = set(states)
    stack = list(states)
    
    while stack:
        s = stack.pop()
        if None in s.transitions:
            for next_s in s.transitions[None]:
                if next_s not in closure:
                    closure.add(next_s)
                    stack.append(next_s)
    return frozenset(closure)
    
def get_symbols(nfa):
    symbols = set()
    for s in nfa.get_states(): 
        for symbol in s.transitions.keys():
            if symbol is not None: 
                symbols.add(symbol)
    return frozenset(symbols)
    
def move(states, symbol):
    result = set()
    for s in states:
        if symbol in s.transitions:
            for next_s in s.transitions[symbol]:
                result.add(next_s)
    return frozenset(result)

def nfa_to_dfa(nfa):
    symbols = get_symbols(nfa)
    initial_closure = epsilon_closure([nfa.initial])
    initial_dfa_state = state(initial_closure)
    initial_dfa_state.is_accept = nfa.accept in initial_closure

    dfa_states = {initial_dfa_state}
    unmarked_states = [initial_dfa_state]
    state_map = {initial_closure: initial_dfa_state}

    while unmarked_states:
        current_dfa_state = unmarked_states.pop()

        for symbol in symbols:
            moved_states = move(current_dfa_state.nfa_states, symbol)
            if moved_states:
                closure = epsilon_closure(moved_states)

                if closure in state_map:
                    next_dfa_state = state_map[closure]
                else:
                    next_dfa_state = state(closure)
                    next_dfa_state.is_accept = nfa.accept in closure

                    dfa_states.add(next_dfa_state)
                    unmarked_states.append(next_dfa_state)
                    state_map[closure] = next_dfa_state

                current_dfa_state.transitions[symbol] = next_dfa_state

    accept_states = {s for s in dfa_states if s.is_accept}

    return dfa(initial_dfa_state, accept_states)
    
def match_string(dfa, input_string):
    current_state = dfa.initial
    print(f"\nMatching string '{input_string}' starting from DFA state ID: {current_state.id}")
    for i, symbol in enumerate(input_string):
        print(f"  Processing symbol '{symbol}' (index {i}). Current DFA state ID: {current_state.id}")
        if symbol in current_state.transitions:
            next_state = current_state.transitions[symbol]
            print(f"    Transition for '{symbol}' to DFA state ID: {next_state.id}")
            current_state = next_state
        else:
            print(f"    NO TRANSITION for '{symbol}' from DFA state ID: {current_state.id}. Match failed.")
            return False

    print(f"End of string. Final DFA state ID: {current_state.id}. Is accept state? {current_state.is_accept}")
    return current_state.is_accept
