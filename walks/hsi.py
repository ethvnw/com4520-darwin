from itertools import product 

from fsm_gen.generator import FSMGenerator 

"""
Utility functions with the capability for computation of H-sets, W-sets and HSI suites.
"""


def _find_shortest_path(fsm: FSMGenerator, end: str) -> list:
    """
    Find the shortest path from the initial state to the end state.
    
    Args:
        fsm (FSMGenerator): the FSM to find the shortest path in
        end (str): the end state

    Returns:
        list: the shortest path from the initial state to the end state
    """
    queue = [(fsm.states[0], [])]
    while queue:
        (state, path) = queue.pop(0)
        transitions = fsm._get_transitions(source=state)
        for transition in transitions:
            inp = transition["trigger"].split(" / ")[0]
            next_state = transition["dest"]

            if next_state == end:
                return path + [inp]
            else:
                queue.append((next_state, path + [inp]))


def _generate_state_cover(fsm: FSMGenerator) -> dict:
    """
    Generate the state cover for the FSM.

    Args:
        fsm (FSMGenerator): the FSM to generate the state cover for
    
    Returns:
        dict: the state cover for the FSM
    """
    state_cover = {}
    for state in fsm.states[1:]:
        state_cover[state] = _find_shortest_path(fsm, state)

    state_cover[fsm.states[0]] = []

    return state_cover


def _generate_transition_cover(fsm: FSMGenerator) -> set:
    """
    Generate the transition cover for the FSM.
    
    Args:
        fsm (FSMGenerator): the FSM to generate the transition cover for

    Returns:
        set: the transition cover for the FSM
    """
    state_cover = _generate_state_cover(fsm)
    transition_cover = set()

    for state in fsm.states:
        transitions = fsm._get_transitions(source=state)
        for transition in transitions:
            inp = transition["trigger"].split(" / ")[0]
            transition_cover.add(''.join(state_cover[state] + [inp]))

    return transition_cover


def _compute_w_set(fsm: FSMGenerator) -> dict:
    """
    Compute the W set for the FSM.
    
    Args:
        fsm (FSMGenerator): the FSM to compute the W set

    Returns:
        dict: the W set for the FSM
    """
    W = {}
    max_len = 5

    state_pairs = [(s1, s2) for i, s1 in enumerate(fsm.states) for s2 in fsm.states[i+1:]]
    test_sequences = [''.join(seq) for length in range(1, max_len + 1) for seq in product(fsm.events, repeat=length)]

    for s1, s2 in state_pairs:
        for seq in test_sequences:
            _, output1 = fsm.apply_input_sequence(s1, seq)
            _, output2 = fsm.apply_input_sequence(s2, seq)

            if output1 != output2:
                W.setdefault(s1, set()).add(seq)
                W.setdefault(s2, set()).add(seq)
                break

    return W


def _compute_h_sets(fsm: FSMGenerator) -> dict:
    """
    Compute the H set (separating family) for the FSM, ensuring that for each pair of states, 
    there exist sequences with a common prefix that lead to different outputs.

    Args:
        fsm (FSMGenerator): the FSM to compute the H sets for
    
    Returns:
        dict: The H set for the FSM, mapping each state to a minimal set of distinguishing sequences.
    """
    W = _compute_w_set(fsm)
    H = {state: set() for state in fsm.states}
    
    # Find minimal necessary prefixes and ensure the common prefix condition
    for s1, s2 in [(s1, s2) for i, s1 in enumerate(fsm.states) for s2 in fsm.states[i+1:]]:
        minimal_prefixes = set()
        
        for seq1 in sorted(W[s1], key=len):  # Prioritising shorter sequences
            for seq2 in sorted(W[s2], key=len):
                common_prefix = next((seq1[:k] for k in range(1, min(len(seq1), len(seq2)) + 1) if seq1[:k] == seq2[:k]), None)
                
                if common_prefix:
                    _, output1 = fsm.apply_input_sequence(s1, common_prefix)
                    _, output2 = fsm.apply_input_sequence(s2, common_prefix)
                    
                    if output1 != output2:  # Ensure the prefix causes a different output
                        minimal_prefixes.add(common_prefix)
                        break  
        
        # Assign the minimal set to both states
        H[s1] |= minimal_prefixes
        H[s2] |= minimal_prefixes

    return H


def generate_HSI_suite(fsm: FSMGenerator) -> dict:
    """
    Generate the HSI suite for the FSM, which is the transition cover appended with the H sets.

    Args:
        fsm (FSMGenerator): the FSM to generate the HSI suite for
    
    Returns:
        dict: the HSI suite for the FSM
    """
    test_suite = {}
    H_sets = _compute_h_sets(fsm)
    transition_cover = _generate_transition_cover(fsm)

    for inp in transition_cover:
        state, _ = fsm.apply_input_sequence(fsm.states[0], inp)

        for seq in H_sets[state]:
            test_suite[inp + seq] = fsm.apply_input_sequence(fsm.states[0], inp + seq)[1]

    return test_suite
