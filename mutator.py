import os
import pickle
import random

from random_gen import FSMGenerator
from machine import Machine


class Mutator:
    MUTATION_TYPES = ['add_state', 'change_trigger_output', 'change_trans_dest']


    def __init__(self, fsm: FSMGenerator) -> None:
        self.fsm = fsm
        self.num_mutations = int(0.4 * len(self.fsm.states))
        self.mutations_applied = []
        self._create_mutated_fsm()


    def _create_mutated_fsm(self):
        self._mutate()
        self.fsm.machine = Machine(states=self.fsm.states, initial=self.fsm.states[0],
                                   graph_engine="pygraphviz", auto_transitions=False,
                                   transitions=self.fsm.transitions)
        
        if not os.path.exists('fsm_imgs/mutated'):
            os.makedirs('fsm_imgs/mutated')
        self.fsm.draw(f'fsm_imgs/mutated/mutated.png')
        
        if not os.path.exists('pickles/mutated'):
            os.makedirs('pickles/mutated')    
        pickle.dump(self.fsm, open(f'pickles/mutated/mutated.pkl', 'wb'))


    def _mutate(self):
        for _ in range(self.num_mutations):
            mutation = random.choice(self.MUTATION_TYPES)

            match mutation:
                case 'add_state':
                    self._add_state()
                case 'remove_state':
                    self._remove_state()
                case 'change_trigger_output':
                    self._change_trigger_output()
                case 'change_trans_dest':
                    self._change_trans_dest()

        print("Mutations applied:")
        for mutation in self.mutations_applied:
            print(f"\t{mutation}")
        self.get_machine_properties()

    
    def _add_state(self):
        # Get random source state and transition
        source_state = random.choice(self.fsm.states)
        source_state_trans = random.choice([t for t in self.fsm.transitions if t["source"] == source_state])

        # Create new state
        last_state_num = self.fsm.states[-1][1:]
        new_state = f'S{int(last_state_num) + 1}'
        self.fsm.states.append(new_state)

        # Add new transition from new state to dest of source_state
        # Modify source_state transition to point to new state
        used_event = random.choice(self.fsm.events)
        self.fsm.transitions.append({
            "source": new_state,
            "trigger": used_event + ' / ' + str(random.randint(0, 1)),
            "dest": source_state_trans["dest"]
        })
        source_state_trans["dest"] = new_state

        # Add transitions from new state to other states for remaining events
        for event in self.fsm.events:
            if event != used_event:
                self.fsm.transitions.append({
                    "source": new_state,
                    "trigger": event + ' / ' + str(random.randint(0, 1)),
                    "dest": random.choice(self.fsm.states)
                })

        self.mutations_applied.append(f"Added state {new_state} using {source_state_trans}")
    

    # TODO: Implement remove_state
    def _remove_state(self):
        pass


    def _change_trigger_output(self):
        transition = random.choice(self.fsm.transitions)
        self.mutations_applied.append(f"Changed trigger output of transition {transition}")

        transition_trigger = transition["trigger"].split(' / ')
        transition["trigger"] = f'{transition_trigger[0]} / {1 - int(transition_trigger[1])}'



    def _get_num_incoming_transitions(self, state):
        num_incoming = 0

        for transition in self.fsm.transitions:
            if transition["dest"] == state:
                num_incoming +=1

        return num_incoming

    
    def _change_trans_dest(self):
        transition = random.choice(self.fsm.transitions)

        # ensures fsm is connected still
        while self._get_num_incoming_transitions(transition["dest"]) < 2:
            transition = random.choice(self.fsm.transitions)
        self.mutations_applied.append(f"Changed destination of transition {transition}")

        transition["dest"] = random.choice(self.fsm.states)


    def _check_determinism(self):
        for state in self.fsm.states:
            transitions = [t for t in self.fsm.transitions if t["source"] == state]
            triggers = [t["trigger"].split(' / ')[0] for t in transitions]
            if len(triggers) != len(set(triggers)):
                return False
            
        return True


    def get_machine_properties(self):
        connected = self.fsm.ensure_connected_machine()
        deterministic = self._check_determinism()

        print(f"\nConnected: {connected}, Deterministic: {deterministic}")