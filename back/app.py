from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from parser import parse_to_rpn
from nfa import compile as compileNfa
from dfa import nfa_to_dfa, match_string, state as DfaState

app = Flask(__name__, template_folder='../front')

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
        state_to_id_map = {s: i for i, s in enumerate(sorted(list(dfa_obj.states), key=lambda x: x.id))}
        for s in dfa_obj.states:
            dfa_states_data.append(state_to_id_map[s])
            for symbol, next_state in s.transitions.items():
                dfa_transitions_data.append({
                    "from":state_to_id_map[s],
                    "to":state_to_id_map[next_state],
                    "symbol":symbol
                })
        initial_state_id = state_to_id_map[dfa_obj.initial]
        accept_states_ids = [state_to_id_map[s] for s in dfa_obj.accept_states]

        match_result = None
        if test_string:
            match_result = match_string(dfa_obj, test_string)

        return jsonify({
            "states": dfa_states_data,
            "transitions": dfa_transitions_data,
            "initial": initial_state_id,
            "accept": accept_states_ids,
            "matchResult": match_result
        })
    except Exception as e:
        print(f"Greska prilikom obrade: {e}")
        return jsonify({"error":str(e)}),500

if __name__ == '__main__':
    print("server se pokrece")
    app.run(debug=True)