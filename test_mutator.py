from random_gen import FSMGenerator
from mutator import Mutator

fsm = FSMGenerator(num_states=5, num_inputs=3)
fsm.draw("normal.png")
mutator = Mutator(fsm)
