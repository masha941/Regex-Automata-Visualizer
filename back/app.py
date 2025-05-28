# app.py

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from parser import parse_to_rpn
from nfa import compile as compileNfa
from dfa import nfa_to_dfa, match_string

app = Flask(__name__, template_folder='../front')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visualize', methods=['POST'])
def visualize():
    data = request.json
    regex_pattern = data.get('regex')
    test_string = data.get('testString')

    if not regex_pattern:
        return jsonify({"error":"Regular expression is required."}),400
    
    try:
        rpn = parse_to_rpn(regex_pattern)
        nfa_obj = compileNfa(rpn)
        dfa_obj = nfa_to_dfa(nfa_obj)
        
        dfa_states_data = []
        dfa_transitions_data = []
        
        # OVO JE KLJUČNA PROMENA SORTIRANJA:
        # Pretpostavka: s.nfa_states je frozenset NFAState objekata.
        # Pretpostavka: NFAState objekti imaju atribut 'id' (npr. n_state.id).
        # Ako NFAState objekti nemaju 'id', onda morate koristiti nešto drugo što ih jedinstveno identifikuje
        # (npr. str(n_state) ako __str__ daje jedinstvenu reprezentaciju).
        
        sorted_dfa_states = sorted(
            list(dfa_obj.states),
            key=lambda s: tuple(sorted([n_state.id for n_state in s.nfa_states])) # Kljuc je SORTIRANI TUPLE NFA ID-jeva
        )
        
        state_internal_id_to_display_id_map = {s.id: i for i, s in enumerate(sorted_dfa_states)}
        
        for s in sorted_dfa_states:
            display_id = state_internal_id_to_display_id_map[s.id]
            dfa_states_data.append({
                "id": display_id,
                "label": f"q{display_id}"
            })

        for s in sorted_dfa_states:
            for symbol, next_dfa_state in s.transitions.items():
                transition_label = str(symbol) if symbol is not None else "\u03B5"
                
                dfa_transitions_data.append({
                    "from": state_internal_id_to_display_id_map[s.id],
                    "to": state_internal_id_to_display_id_map[next_dfa_state.id],
                    "label": transition_label
                })
        
        initial_state_display_id = state_internal_id_to_display_id_map[dfa_obj.initial.id]
        accept_states_display_ids = [state_internal_id_to_display_id_map[s.id] for s in dfa_obj.accept_states]

        match_result = None
        if test_string:
            match_result = match_string(dfa_obj, test_string)

        # DEBUG INFO
        print("\n--- DFA Debug Info (from app.py) ---")
        print(f"Regex: '{regex_pattern}'")
        print(f"Test String: '{test_string}'")
        print(f"Match Result: {match_result}")
        print("DFA States data sent:")
        for state_data in dfa_states_data:
            print(f"  {state_data}")
        print("DFA Transitions data sent:")
        for trans_data in dfa_transitions_data:
            print(f"  {trans_data}")
        print("Initial state display ID:", initial_state_display_id)
        print("Accept states display IDs:", accept_states_display_ids)
        print("--- End Debug Info ---\n")

        return jsonify({
            "states": dfa_states_data,
            "transitions": dfa_transitions_data,
            "initial": initial_state_display_id,
            "accept": accept_states_display_ids,
            "matchResult": match_result
        })
    except Exception as e:
        print(f"Greska prilikom obrade: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error":str(e)}),500

if __name__ == '__main__':
    print("server se pokrece")
    app.run(debug=True)