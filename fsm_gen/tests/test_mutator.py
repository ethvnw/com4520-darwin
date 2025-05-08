import os
import pickle

import pytest
import collections
import random
import pickle
import os
import re
from fsm_gen.generator import FSMGenerator
from fsm_gen.mutator import Mutator


@pytest.fixture
def testing_fsm():
    fsm = FSMGenerator(num_states=5, num_inputs=3, num_outputs=2)
    fsm.draw("original.png")
    return fsm


@pytest.fixture
def mutator(testing_fsm):
    return Mutator(testing_fsm)


@pytest.fixture
def mutated_fsm(mutator):
    mutator.create_mutated_fsm()
    return mutator.fsm

def test_add_state():
    """Ensure the mutator correctly adds a state"""
    fsm = FSMGenerator(num_states=5, num_inputs=3, num_outputs=2)
    mutator = Mutator(fsm)
    initial_state_count = len(fsm.states)
    mutator._add_state()
    assert len(mutator.fsm.states) > initial_state_count

def test_remove_state():
    """Ensure the mutator correctly removes a state"""
    fsm = FSMGenerator(num_states=5, num_inputs=3, num_outputs=2)
    mutator = Mutator(fsm)
    initial_state_count = len(fsm.states)
    mutator._remove_state()
    assert len(mutator.fsm.states) < initial_state_count
    




def test_change_trigger_output():
    """Ensure the change trigger output mutation is correctly applied"""
    fsm = FSMGenerator(num_states=5, num_inputs=3,num_outputs=2)
    mutator = Mutator(fsm)

    initial_triggers = [t["trigger"] for t in fsm.transitions]
    mutated = mutator._change_trigger_output()

    assert not(mutated["trigger"] not in initial_triggers)

def test_change_trans_dest():
    """Ensure the change transition destination mutation is correctly applied"""
    fsm = FSMGenerator(num_states=5, num_inputs=3, num_outputs=2)
    mutator = Mutator(fsm)

    original_transitions = [dict(t) for t in fsm.transitions]
    mutated_transition = mutator._change_trans_dest()

    for original in original_transitions:
        if (original["trigger"] == mutated_transition["trigger"] and
            original["source"] == mutated_transition["source"]):
            assert original["dest"] != mutated_transition["dest"]
            break
    else:
        assert False

def test_create_mutated_fsm(mutated_fsm):
    """Ensure the mutator correctly produces the files needed"""
    mutated_fsm.draw("mutated.png")
    with open("mutated.pkl", "wb") as f:
        pickle.dump(mutated_fsm, f)
    assert isinstance(mutated_fsm, FSMGenerator)
    assert os.path.exists("mutated.pkl")

def test_mutation_application(mutator, testing_fsm):
    """Ensure the mutator doesnt mutate back to the original FSM"""
    original_fsm = pickle.dumps(testing_fsm)
    mutator.create_mutated_fsm()
    assert mutator.mutations_applied
    assert pickle.dumps(mutator.fsm) != original_fsm
    
def test_get_num_transitions_exclude_loops(mutator):
    """Ensure the number of transitions is counted correctly"""
    fsm = FSMGenerator(num_inputs=1,num_states=1, num_outputs=2)
    mutator = Mutator(fsm)
    assert 0 == mutator._get_num_transitions_exclude_loops(fsm.transitions[0]["dest"],True)

@pytest.fixture(scope="function", autouse=True)
def cleanup():
    yield
    for file in ["original.png", "mutated.png", "mutated.pkl"]:
        if os.path.exists(file):
            os.remove(file)

## mutator ##
# add state #
# remove state # 
# change trigger output # 
# change transition destination # 

## all mutator functions ##

# create_mutated_fsm() # done

# _mutate() # done

# _add_state() # done

# _remove_state() # done

# _change_trigger_output() # done

# _get_num_transitions_exclude_loops() ?

# _change_trans_dest() # done

# _check determinism() # tested elsewhere

# _check connectivity() # tested elsewhere

    # dfs() # tested elsewhere

# get_machine_properties() # only prints previous 2 function outputs
