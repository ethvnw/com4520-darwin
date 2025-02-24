from fsm_gen.generator import FSMGenerator
from fsm_gen.mutator import Mutator

fsm = FSMGenerator(num_states=5, num_inputs=3)
fsm.draw("original.png")

mutated_fsm = Mutator(fsm).create_mutated_fsm()
mutated_fsm.draw("mutated.png")