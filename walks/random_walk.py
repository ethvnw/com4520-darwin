import random
from enum import Enum

from fsm_gen.generator import FSMGenerator


class RandomWalk:
    class WalkType(Enum): 
        RANDOM = 0
        RANDOM_WITH_RESET = 1
        LIMITED_SELF_LOOP = 2
        STATISTICAL = 3

    
    def __init__(self, fsm: FSMGenerator, target_coverage: int, HSI_suite: dict) -> None:
        self.fsm = fsm
        self.target_coverage = target_coverage
        self.transitions_length = len(fsm.transitions)
        self.HSI_suite = HSI_suite


    def walk(self, walk_type) -> int:
        self.fsm.machine.state = self.fsm.machine.initial
        if walk_type == self.WalkType.RANDOM:
            result = self.random_walk()
        elif walk_type == self.WalkType.RANDOM_WITH_RESET:
            result = self.random_walk_with_reset(5)
        elif walk_type == self.WalkType.LIMITED_SELF_LOOP:
            result = self.limited_self_loop_walk()
        elif walk_type == self.WalkType.STATISTICAL:
            result = self.statistical_walk()
        return result
    

    def statistical_walk(self) -> int:
        transitions_executed = set()
        coverage = 0
        state = self.fsm.machine.initial
        walk = []

        input_probabilities = []
        probabilities = [random.random() for i in range(0, len(self.fsm.events))]
        summed_probabilities = sum(probabilities)
        for i in range(0, len(probabilities)):
            input_probabilities.append(probabilities[i] / summed_probabilities)

        while coverage < self.target_coverage:
            triggers = self.fsm._get_triggers(state)
            trigger = random.choices(triggers, input_probabilities, k=1)[0]

            self.fsm.machine.trigger(trigger)
            transitions_executed.add(f"{state}->{trigger}")
            walk.append(f"{state}->{trigger}")

            state = self.fsm.machine.state
            coverage = len(transitions_executed) / self.transitions_length * 100

        return len(walk)


    def limited_self_loop_walk(self) -> int:
        transitions_executed = set()
        coverage = 0
        state = self.fsm.machine.initial
        walk = []
        self_loop_triggers = []

        while coverage < self.target_coverage:
            triggers = self.fsm._get_triggers(state)

            # Limit triggers to those that are not already explored self-loops
            triggers_excluding_self_loops = [t for t in triggers if [state, t] not in self_loop_triggers]
            if len(triggers_excluding_self_loops) != 0:
                trigger = random.choice(triggers_excluding_self_loops)
            # Fallback incase only option is to self-loop (theoretically impossible in connected machine)
            else:
                trigger = random.choice(triggers)
            previous_state = self.fsm.machine.state

            self.fsm.machine.trigger(trigger)
            transitions_executed.add(f"{state}->{trigger}")
            walk.append(f"{state}->{trigger}")

            state = self.fsm.machine.state
            current_state = self.fsm.machine.state

            # Record presence of a self-loop and the trigger it is associated with
            if previous_state == current_state and [state, trigger] not in self_loop_triggers:
                self_loop_triggers.append([state, trigger])

            coverage = len(transitions_executed) / self.transitions_length * 100

        return len(walk)


    def random_walk_with_reset(self, step_limit: int) -> int:
        walk = []
        walk_since_reset = []
        steps_since_identification = 0
        coverage = 0
        state = self.fsm.machine.initial
        transitions_executed = set()

        while coverage < self.target_coverage:
            triggers = self.fsm._get_triggers(state)
            trigger = random.choice(triggers)

            self.fsm.machine.trigger(trigger)
            transitions_executed.add(f"{state}->{trigger}")
            walk.append(f"{state}->{trigger}")
            walk_since_reset.append(f"{state}->{trigger}")

            for index, input_seq in enumerate(self.HSI_suite.keys()):
                io_sequence = {}
                key = ""
                outputs = ()
                for pair in walk_since_reset[:len(input_seq)]:
                    io = pair.split("->")[1].split(" / ")
                    if len(io) == 2:
                        key += str(io[0])
                        outputs += (io[1],)
                io_sequence[key] = outputs

                if key in self.HSI_suite.keys() and io_sequence[key] == self.HSI_suite[input_seq]:
                    break
                elif index == len(self.HSI_suite) - 1:
                    steps_since_identification += 1
                    print ("Steps since identification: " + str(steps_since_identification))

            if steps_since_identification >= step_limit:
                self.fsm.machine.state = self.fsm.machine.initial
                walk_since_reset = []
                steps_since_identification = 0

            state = self.fsm.machine.state
            coverage = len(transitions_executed) / self.transitions_length * 100

        return len(walk)
    

    def random_walk(self) -> int:
        transitions_executed = set()
        coverage = 0
        state = self.fsm.machine.initial
        walk = []

        while coverage < self.target_coverage:
            triggers = self.fsm._get_triggers(state)
            trigger = random.choice(triggers)

            self.fsm.machine.trigger(trigger)
            transitions_executed.add(f"{state}->{trigger}")
            walk.append(f"{state}->{trigger}")

            state = self.fsm.machine.state
            coverage = len(transitions_executed) / self.transitions_length * 100

        return len(walk)
