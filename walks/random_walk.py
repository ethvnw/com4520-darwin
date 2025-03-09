import random
from enum import Enum

from fsm_gen.machine import Machine


class RandomWalk:
    class WalkType(Enum): 
        RANDOM = 0
        GREEDY = 1
        CLOSEST_FIRST = 2

    
    def __init__(self, fsm: Machine, walk_type: WalkType, target_coverage: int) -> None:
        self.fsm = fsm
        self.type = walk_type
        self.target_coverage = target_coverage
        self.transitions_length = len(fsm.get_transitions())


    def walk(self) -> int:
        if self.type == self.WalkType.RANDOM:
            result = self.random_walk()
        elif self.type == self.WalkType.GREEDY:
            result = self.greedy_walk()
        elif self.type == self.WalkType.CLOSEST_FIRST:
            result = self.closest_first_walk()

        return result

    def random_walk(self) -> int:
        transitions_executed = set()
        coverage = 0
        state = self.fsm.initial
        walk = []

        while coverage < self.target_coverage:
            triggers = self.fsm.get_triggers(state)
            trigger = random.choice(triggers)

            self.fsm.trigger(trigger)
            transitions_executed.add(f"{state}->{trigger}")
            walk.append(f"{state}->{trigger}")

            state = self.fsm.state
            coverage = len(transitions_executed) / self.transitions_length * 100

    
        return len(walk)
