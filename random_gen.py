import os
import pickle
import random

from machine import Machine


class RandomGenerator:
    ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    
    MAX_NUM_STATES = 5
    MAX_ALPHABET_LENGTH = 4
    
    def __init__(self) -> None:
        self.states = [f'S{i}' for i in range(random.randint(
            3, 
            RandomGenerator.MAX_NUM_STATES))]
        
        self.events = [RandomGenerator.ALPHABET[i] for i in range(random.randint(
            2, 
            RandomGenerator.MAX_ALPHABET_LENGTH))]
        
        self._try_generate_connected_machine()
        print(f"Machine with {len(self.states)} states and {len(self.events)} events created.")
        self.get_equivalent_states()

    
    def _try_generate_connected_machine(self) -> None:
        connected = False

        while not connected:
            self.transitions = self._generate_transitions()        
            self.machine = Machine(states=self.states, 
                                    initial=self.states[0], graph_engine='pygraphviz', 
                                    auto_transitions=False, transitions=self.transitions)

            connected = self._ensure_connected_machine()


    def _generate_transitions(self) -> list:
        """
        Generate random transitions between states.

        Returns:
            list: A list of dictionaries representing the transitions.
        """
        transitions = []

        for state in self.states:
            events = random.sample(self.events, len(self.events) - 1)
            for event in events:
                dest = random.choice(self.states)
        
                transitions.append({
                    'trigger': event + ' / ' + str(random.randint(0, 1)),
                    'source': state,
                    'dest': dest
                })

        return transitions


    def _is_reachable_from(self, state: str, target: str) -> bool:
        """
        Check if a target state is reachable from a given state.

        Args:
            state (str): The source state.
            target (str): The target state.

        Returns:
            bool: True if the target state is reachable from the source state, False otherwise.
        """
        reachable_states = set()
        states_to_check = [state]

        while states_to_check:
            current_state = states_to_check.pop()

            if current_state == target:
                return True
            
            for transition in self.transitions:
                if transition['source'] == current_state and transition['dest'] not in reachable_states:
                    reachable_states.add(transition['dest'])
                    states_to_check.append(transition['dest'])

        return False
    

    def _add_leftover_transitions(self) -> None:
        """
        Add any transitions that are missing for an event to make the machine complete.
        """
        for state in self.states:
            current_triggers = [trigger[0] for trigger in self.machine.get_triggers(state) ]
            available_triggers = [event for event in self.events if event not in current_triggers]

            for trigger in available_triggers:
                dest = random.choice(self.states)

                self.machine.add_transition(
                    trigger=trigger + ' / ' + str(random.randint(0, 1)),
                    source=state,
                    dest=dest
                )
        

    def _ensure_connected_machine(self) -> bool:
        """
        Ensure that all states are reachable from any other state.

        Returns:
            bool: True if the machine is connected, False otherwise.
        """
        for state in self.states:
            for target in self.states:
                if state == target:
                    continue

                if not self._is_reachable_from(state, target):
                    current_triggers = [trigger[0] for trigger in self.machine.get_triggers(state) ]
                    available_triggers = [event for event in self.events if event not in current_triggers]

                    if not available_triggers:
                        return False

                    self.machine.add_transition(
                        trigger=available_triggers[0] + ' / ' + str(random.randint(0, 1)),
                        source=state,
                        dest=target
                    )

        self._add_leftover_transitions()
        return True
    

    def get_equivalent_states(self) -> None:
        for state1 in self.states:
            for state2 in self.states:
                if state1 == state2:
                    continue

                state1_transitions = self.machine.get_triggers(state1)
                state2_transitions = self.machine.get_triggers(state2)

                if state1_transitions == state2_transitions:
                    print(f"States {state1} and {state2} are equivalent.")
                    print(f"State {state1} transitions: {state1_transitions}")
                    print(f"State {state2} transitions: {state2_transitions}")


        
if __name__ == '__main__':
    random_fsm = RandomGenerator()
    random_fsm.machine.get_graph().draw('random_fsm.png', prog='dot')

    num_pickles = len([file for file in os.listdir('pickles')])
    pickle.dump(random_fsm, open(f'pickles/random_fsm_{num_pickles}.pkl', 'wb'))