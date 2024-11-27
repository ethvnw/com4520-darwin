import argparse
import pickle
import random

from random_gen import RandomGenerator
from machine import Machine


class Mutator:
    STATE_MUTATION_TYPES = ['add_state', 'remove_state']
    TRANSITION_MUTATION_TYPES = ['change_trigger_input', 'change_trigger_output', 'change_source', 'change_dest']
    MUTATION_PROBABILITY = 0.2


    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description='Mutator')
        parser.add_argument('--machine', type=str, help='Path to the machine pickle file')
        args = parser.parse_args()

        if args.machine is None:
            raise Exception('Path to the machine pickle file is required')

        self.fsm = pickle.load(open(args.machine, 'rb'))
        self.fsm.machine.get_graph().draw('original_fsm.png', prog='dot')
        self._create_mutated_fsm()
        pickle.dump(self.fsm, open('mutated_machine.pkl', 'wb'))

    def _create_mutated_fsm(self):
        self._mutate()
        self.fsm.machine = Machine(states=self.fsm.states, initial=self.fsm.states[0],
                                   graph_engine="pygraphviz", auto_transitions=False,
                                   transitions=self.fsm.transitions)
        self.fsm.machine.get_graph().draw('mutated_fsm.png', prog='dot')


    def _mutate(self):
        for state in self.fsm.states:
            if random.random() < self.MUTATION_PROBABILITY:
                self._mutate_state(state)

        for transition in self.fsm.transitions:
            if random.random() < self.MUTATION_PROBABILITY:
                self._mutate_transition(transition)

    
    def _generate_state(self) -> str:
        last_state_num = self.fsm.states[-1][1:]
        return f'S{int(last_state_num) + 1}'


    def _mutate_state(self, state: str) -> None:
        mutation_type = random.choice(self.STATE_MUTATION_TYPES)

        if mutation_type == 'add_state':
            self.fsm.states.append(self._generate_state())
        elif mutation_type == 'remove_state':
            self.fsm.states.remove(state)


    def _mutate_transition(self, transition: dict) -> None:
        mutation_type = random.choice(self.TRANSITION_MUTATION_TYPES)
        transition_trigger = transition["trigger"].split(' / ')

        if mutation_type == 'change_trigger_input':
            transition["trigger"] = f'{random.choice(self.fsm.events)} / {transition_trigger[1]}'
        elif mutation_type == 'change_trigger_output':
            transition["trigger"] = f'{transition_trigger[0]} / {random.randint(0, 1)}'
        elif mutation_type == 'change_source':
            transition["source"] = random.choice(self.fsm.states)
        elif mutation_type == 'change_dest':
            transition["dest"] = random.choice(self.fsm.states)


if __name__ == '__main__':
    Mutator()