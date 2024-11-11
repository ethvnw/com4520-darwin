import os
import pickle
import random

from transitions.extensions import GraphMachine

# TODO: Apply the W set to remove equivalent states

class RandomFSMGenerator:
    ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    
    def __init__(self) -> None:
        self.states = [f'S{i}' for i in range(random.randint(11, 20))]
        self.inputs = [RandomFSMGenerator.ALPHABET[i] for i in range(random.randint(5, 20))]
        self.transitions = []
        self.generate_transitions()

        self.machine = GraphMachine(model=self, states=self.states, 
                                    initial=self.states[0], transitions=self.transitions,
                                    graph_engine='pygraphviz')
        

    def generate_transitions(self) -> None:
        for state in self.states:
            num_transitions = random.randint(1, len(self.inputs))
            inputs = random.sample(self.inputs, num_transitions)

            for inp in inputs:
                dest = random.choice(self.states)

                self.transitions.append({
                    'trigger': inp,
                    'source': state,
                    'dest': dest
                })

   
        self.ensure_connected()
    

    def ensure_connected(self):
        # Use a set to track reachable states
        reachable_states = {self.states[0]}
        states_to_check = [self.states[0]]
        
        # Check reachability using a breadth-first search-like approach
        while states_to_check:
            current_state = states_to_check.pop()
            for transition in self.transitions:
                if transition['source'] == current_state and transition['dest'] not in reachable_states:
                    reachable_states.add(transition['dest'])
                    states_to_check.append(transition['dest'])

        # If any state is not reachable, randomly connect it
        for state in self.states:
            if state not in reachable_states:
                # Add a transition to connect the unconnected state
                self.transitions.append({
                    'trigger': random.choice(self.inputs),
                    'source': random.choice(list(reachable_states)),
                    'dest': state
                })



if __name__ == "__main__":
    fsm = RandomFSMGenerator()
    num_pkls = len([f for f in os.listdir("pickles") if f.endswith('.pkl')])
    with open(f'pickles/random_fsm_{num_pkls + 1}.pkl', 'wb') as f:
        pickle.dump(fsm, f)

    fsm.get_graph().draw('random_fsm.png', prog='dot')