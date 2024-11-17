from machine import Machine

from transitions import Transition

class Basic_FSM(object):

    states = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    inputs = ['0', '1']

    def __init__(self, name):

        self.name = name
        self.machine = Machine(model=self, states=Basic_FSM.states, initial='A', auto_transitions=False)

        self.machine.add_transition(trigger="0 / 0", source='A', dest='F')
        self.machine.add_transition(trigger="0 / 0", source='B', dest='G')
        self.machine.add_transition(trigger="0 / 0", source='C', dest='B')
        self.machine.add_transition(trigger="0 / 0", source='D', dest='C')
        self.machine.add_transition(trigger="0 / 0", source='E', dest='D')
        self.machine.add_transition(trigger="0 / 1", source='F', dest='E')
        self.machine.add_transition(trigger="0 / 1", source='G', dest='E')

        self.machine.add_transition(trigger="1 / 1", source='A', dest='B')
        self.machine.add_transition(trigger="1 / 1", source='B', dest='A')
        self.machine.add_transition(trigger="1 / 1", source='C', dest='C')
        self.machine.add_transition(trigger="1 / 1", source='D', dest='B')
        self.machine.add_transition(trigger="1 / 1", source='E', dest='A')
        self.machine.add_transition(trigger="1 / 1", source='F', dest='F')
        self.machine.add_transition(trigger="1 / 1", source='G', dest='G')

        self.transitions = [
            {'trigger': '0 / 0', 'source': 'A', 'dest': 'F'}, 
            {'trigger': '0 / 0', 'source': 'B', 'dest': 'G'}, 
            {'trigger': '0 / 0', 'source': 'C', 'dest': 'B'}, 
            {'trigger': '0 / 0', 'source': 'D', 'dest': 'C'},
            {'trigger': '0 / 0', 'source': 'E', 'dest': 'D'},
            {'trigger': '0 / 1', 'source': 'F', 'dest': 'E'},
            {'trigger': '0 / 1', 'source': 'G', 'dest': 'E'},
            {'trigger': '1 / 1', 'source': 'A', 'dest': 'B'},
            {'trigger': '1 / 1', 'source': 'B', 'dest': 'A'},
            {'trigger': '1 / 1', 'source': 'C', 'dest': 'C'},
            {'trigger': '1 / 1', 'source': 'D', 'dest': 'B'},
            {'trigger': '1 / 1', 'source': 'E', 'dest': 'A'},
            {'trigger': '1 / 1', 'source': 'F', 'dest': 'F'},
            {'trigger': '1 / 1', 'source': 'G', 'dest': 'G'}
        ]
            


    def _convert_dict_to_set(self, dictionary: dict) -> list:
        combined_sets = []
        for eq_set in dictionary.values():
            combined_sets.append(eq_set)
        return combined_sets


    def _make_1_equivalent(self) -> list:
        equivalence_sets = dict()

        for state in self.states:
            transitions = self.machine.get_triggers(state)

            io_string = ""
            for transition in transitions:
                io_string += transition

            if io_string not in equivalence_sets.keys():
                equivalence_sets[io_string] = set()
                
            equivalence_sets[io_string].add(state)

        return self._convert_dict_to_set(equivalence_sets)



    def _find_equivalent_states(self) -> list:
        previous_equivalence_set = self._make_1_equivalent()
        current_equivalence_set = []

        while True:
            current_equivalence_dict = dict()
            for eq_set in previous_equivalence_set:
                for state in eq_set:
                    triggers = self.machine.get_triggers(state)
                    subset_pointer = ""

                    for trigger in triggers:
                        input_output = trigger.split(" / ")
                        subset_pointer += input_output[0]

                        dest = self.machine.events[trigger].transitions[state][0].dest
                        for index in range(len(previous_equivalence_set)):
                            if dest in previous_equivalence_set[index]:
                                subset_pointer += str(index)
                                break

                    if subset_pointer not in current_equivalence_dict.keys():
                        current_equivalence_dict[subset_pointer] = set()
                
                    current_equivalence_dict[subset_pointer].add(state)
                            
            current_equivalence_set = self._convert_dict_to_set(current_equivalence_dict)
                    
            if current_equivalence_set == previous_equivalence_set:
                break

            previous_equivalence_set = current_equivalence_set

        equivalent_states = []
        for eq_set in current_equivalence_set:
            if len(eq_set) > 1:
                equivalent_states.append(eq_set)

        print (equivalent_states)
        return equivalent_states


    def make_minimal(self) -> None:
        equivalence_states = self._find_equivalent_states()
        for eq_set in equivalence_states:
            for state in eq_set:
                if state != eq_set[0]:
                    pass


if __name__ == "__main__":
    basic = Basic_FSM("testing")
    basic.get_graph().draw('test.png', prog='dot')
    # transitions = basic.machine.get_transitions(source='A')
    # triggers = basic.machine.get_triggers('A')
    # print(transitions[0])
    # print(triggers[0])
    basic._find_equivalent_states()

    #                         the trigger      the source
    # print(basic.machine.events['0 / 0'].transitions['C'])