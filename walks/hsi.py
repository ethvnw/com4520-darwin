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
    
    
    # TODO: Fix this method
    def compute_hsi_sets(self) -> dict:
        """
        Compute the HSI sets for the FSM.
        
        Returns:
            dict: the HSI sets for the FSM
        """
        W = self.compute_w_set()
        HSI_sets = {state: set() for state in self.fsm.states}  # Initialize empty HSI sets

        # Step 1: Identify harmonized sequences from W
        for state in self.fsm.states:
            # W set sequences that distinguish this state
            hsi_candidates = W.get(state, set())

            # Step 2: Ensure that the selected sequences differentiate all states
            for seq in hsi_candidates:
                for i in range(1, len(seq) + 1):
                    prefix = seq[:i]
                    unique_outputs = set()
                    for s in self.fsm.states:
                        _, output = self.fsm.apply_input_sequence(s, prefix)
                        unique_outputs.add(output)

                    # If the prefix creates different outputs for at least one state, use it
                    if len(unique_outputs) > 1:
                        HSI_sets[state].add(prefix)
                        break  # No need to check longer prefixes

        return HSI_sets
