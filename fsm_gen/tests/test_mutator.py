import pytest
import collections
import random
import pickle
import os

from fsm_gen.generator import FSMGenerator
from fsm_gen.mutator import Mutator

fsm = FSMGenerator(num_states=5, num_inputs=3)
fsm.draw("original.png")

mutated_fsm = Mutator(fsm).create_mutated_fsm()
mutated_fsm.draw("mutated.png")

## mutator ##
# add state #
# remove state # 
# change trigger output # 
# change transition destination # 

## all mutator functions ##

# create_mutated_fsm()

# _mutate()

# _add_state()

# _remove_state()

# _change_trigger_output()

# _get_num_transitions_exclude_loops()

# _change_trans_dest()

# _check determinism()

# _check connectivity()

    # dfs()

# get_machine_properties()
