from itertools import product 

from fsm_gen.generator import FSMGenerator 


class HSI:

    def __init__(self, fsm: FSMGenerator):
        self.fsm = fsm


    def _find_shortest_path(self, end) -> list:
        """
        Find the shortest path from the initial state to the end state.
        
        Args:
            end (str): the end state

        Returns:
            list: the shortest path from the initial state to the end state
        """
        queue = [(self.fsm.states[0], [])]
        while queue:
            (state, path) = queue.pop(0)
            transitions = self.fsm._get_transitions(source=state)
            for transition in transitions:
                inp = transition["trigger"].split(" / ")[0]
                next_state = transition["dest"]

                if next_state == end:
                    return path + [inp]
                else:
                    queue.append((next_state, path + [inp]))


    def _generate_state_cover(self) -> dict:
        """
        Generate the state cover for the FSM.
        
        Returns:
            dict: the state cover for the FSM
        """
        state_cover = {}
        for state in self.fsm.states[1:]:
            state_cover[state] = self._find_shortest_path(state)

        state_cover[self.fsm.states[0]] = []

        return state_cover


    def _generate_transition_cover(self) -> set:
        """
        Generate the transition cover for the FSM.
        
        Returns:
            set: the transition cover for the FSM
        """
        state_cover = self._generate_state_cover()
        transition_cover = set()

        for state in self.fsm.states:
            transitions = self.fsm._get_transitions(source=state)
            for transition in transitions:
                inp = transition["trigger"].split(" / ")[0]
                transition_cover.add(''.join(state_cover[state] + [inp]))

        return transition_cover


    def compute_w_set(self) -> dict:
        """
        Compute the W set for the FSM.
        
        Returns:
            dict: the W set for the FSM
        """
        W = {}
        max_len = 5

        state_pairs = [(s1, s2) for i, s1 in enumerate(self.fsm.states) for s2 in self.fsm.states[i+1:]]
        test_sequences = [''.join(seq) for length in range(1, max_len + 1) for seq in product(self.fsm.events, repeat=length)]

        for s1, s2 in state_pairs:
            for seq in test_sequences:
                _, output1 = self.fsm.apply_input_sequence(s1, seq)
                _, output2 = self.fsm.apply_input_sequence(s2, seq)

                if output1 != output2:
                    W.setdefault(s1, set()).add(seq)
                    W.setdefault(s2, set()).add(seq)
                    break

        return W
    

    # def compute_h_sets(self) -> dict:
    #     """
    #     Compute the H set (separating family) for the FSM using the W set.
        
    #     Returns:
    #         dict: The H set for the FSM, where each state maps to a minimal set of distinguishing sequences.
    #     """
    #     W = self.compute_w_set()
    #     H = {state: set() for state in self.fsm.states}
        
    #     # Step 3: Optimize H by only keeping **minimal necessary prefixes**
    #     for state, sequences in W.items():
    #         minimal_sequences = set()
            
    #         for seq in sorted(sequences, key=len):
    #             # Check if any prefix of `seq` is already in minimal_sequences
    #             if not any(seq.startswith(existing) for existing in minimal_sequences):
    #                 minimal_sequences.add(seq)

    #         H[state] = minimal_sequences

    #     return H


    def compute_h_sets(self) -> dict:
        """
        Compute the H set (separating family) for the FSM, ensuring that for each pair of states, 
        there exist sequences with a common prefix that lead to different outputs.
        
        Returns:
            dict: The H set for the FSM, mapping each state to a minimal set of distinguishing sequences.
        """
        W = self.compute_w_set()
        H = {state: set() for state in self.fsm.states}
        
        # Find minimal necessary prefixes and ensure the common prefix condition
        for s1, s2 in [(s1, s2) for i, s1 in enumerate(self.fsm.states) for s2 in self.fsm.states[i+1:]]:
            minimal_prefixes = set()
            
            for seq1 in sorted(W[s1], key=len):  # Prioritising shorter sequences
                for seq2 in sorted(W[s2], key=len):
                    common_prefix = next((seq1[:k] for k in range(1, min(len(seq1), len(seq2)) + 1) if seq1[:k] == seq2[:k]), None)
                    
                    if common_prefix:
                        _, output1 = self.fsm.apply_input_sequence(s1, common_prefix)
                        _, output2 = self.fsm.apply_input_sequence(s2, common_prefix)
                        
                        if output1 != output2:  # Ensure the prefix causes a different output
                            minimal_prefixes.add(common_prefix)
                            break  
            
            # Assign the minimal set to both states
            H[s1] |= minimal_prefixes
            H[s2] |= minimal_prefixes

        return H
