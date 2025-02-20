from machine import Machine
from random_gen import FSMGenerator
from itertools import product

class HSI:

    def __init__(self, fsm: FSMGenerator):
        self.fsm = fsm


    def compute_w_set(self) -> dict:
        W = {}
        max_len = 5

        state_pairs = [(s1, s2) for s1 in self.fsm.states for s2 in self.fsm.states if s1 != s2]
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
    

    def compute_hsi_sets(self) -> dict:
        W = self.compute_w_set()
        HSI_sets = {state: set() for state in self.fsm.states}  # Initialize empty HSI sets

        # Step 1: Identify harmonized sequences from W
        for state in self.fsm.states:
            # W set sequences that distinguish this state
            hsi_candidates = W.get(state, set())

            # Step 2: Ensure that the selected sequences differentiate all states
            for seq in hsi_candidates:
                unique_outputs = set()
                for s in self.fsm.states:
                    _, output = self.fsm.apply_input_sequence(s, seq)
                    unique_outputs.add(output)

                # If the sequence creates different outputs for at least one state, use it
                if len(unique_outputs) > 1:
                    HSI_sets[state].add(seq)

        return HSI_sets



fsm = FSMGenerator(10, 2)
# fsm.transitions = [
#     {"source": "S1",
#      "trigger": "a / 1",
#      "dest": "S2"},

#     {"source": "S1",
#     "trigger": "b / 0",
#     "dest": "S1"},

#     {"source": "S1",
#     "trigger": "c / 0",
#     "dest": "S1"},

#     {"source": "S2",
#     "trigger": "a / 0",
#     "dest": "S2"},

#     {"source": "S2",
#     "trigger": "b / 1",
#     "dest": "S3"},

#     {"source": "S2",
#     "trigger": "c / 1",
#     "dest": "S1"},

#     {"source": "S3",
#     "trigger": "a / 1",
#     "dest": "S2"},

#     {"source": "S3",
#     "trigger": "b / 0",
#     "dest": "S3"},

#     {"source": "S3",
#     "trigger": "c / 1",
#     "dest": "S1"}
#     ]
# fsm.states = ["S1", "S2", "S3"]
# fsm.events = ["a", "b", "c"]
# fsm.machine = Machine(states=fsm.states, initial=fsm.states[0],
#                                    graph_engine="pygraphviz", auto_transitions=False,
#                                    transitions=fsm.transitions)

fsm.draw("testing.png")
hsi = HSI(fsm)
print(hsi.compute_w_set())
print(hsi.compute_hsi_sets())

# print(seq[15])
# print(fsm.apply_input_sequence('S1', seq[15]))