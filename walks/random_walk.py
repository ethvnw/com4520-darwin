import random
from enum import Enum

from fsm_gen.generator import FSMGenerator


class RandomWalk:
    class WalkType(Enum): 
        RANDOM = 0
        RANDOM_WITH_RESET = 1
        PROGRESSIVE = 2
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
        return result


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
