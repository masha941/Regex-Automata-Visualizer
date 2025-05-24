from parser import parse_to_rpn
from nfa import compile
from dfa import nfa_to_dfa, match_string


if __name__ == "__main__":
    # Example: Convert regex "a*b" to DFA and test
    regex = "a*b"
    rpn = parse_to_rpn(regex)
    nfa = compile(rpn)
    dfa = nfa_to_dfa(nfa)

    # Test strings
    print(match_string(dfa, "b"))      # True
    print(match_string(dfa, "ab"))     # True  
    print(match_string(dfa, "aaab"))   # True
    print(match_string(dfa, "a"))      # False