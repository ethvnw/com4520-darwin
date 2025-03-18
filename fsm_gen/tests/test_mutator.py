import pytest
import collections
import random
import pickle
import os
from fsm_gen.generator import FSMGenerator
from fsm_gen.machine import Machine
from fsm_gen.mutator import Mutator

@pytest.fixture
def testing_fsm(): # generate fsm of specified states and inputs to mutate from
    fsm = FSMGenerator(num_states=5, num_inputs=3)
    fsm.draw("original.png")
    return fsm

@pytest.fixture
def mutator(testing_fsm): # create an object of the mutator class
    return Mutator(testing_fsm)

@pytest.fixture
def mutated_fsm(mutator): # mutate the testing fsm
    mutator.create_mutated_fsm()
    return mutator.fsm

def test_mutation_effects(): # had 1 error in 1000 test runs
    """Test if all types of mutations are applied by running multiple mutations on fresh FSM instances."""
    mutation_types_encountered = set()
    expected_mutations = {"add_state", "remove_state", "add_transition", "remove_transition", "modify_transition"} ### STILL TO FIX
    for _ in range(20):  # Run multiple mutations to cover all types
        fsm = FSMGenerator(num_states=5, num_inputs=3)  # Create a fresh FSM
        mutator = Mutator(fsm)  # Create a new Mutator instance
        initial_state_count = len(fsm.states)
        initial_transition_count = len(fsm.transitions)
        original_transitions = pickle.dumps(fsm.transitions)
        mutator.create_mutated_fsm()
        if len(mutator.fsm.states) > initial_state_count:
            mutation_types_encountered.add("add_state")
        elif len(mutator.fsm.states) < initial_state_count:
            mutation_types_encountered.add("remove_state")
        if len(mutator.fsm.transitions) > initial_transition_count:
            mutation_types_encountered.add("add_transition")
        elif len(mutator.fsm.transitions) < initial_transition_count:
            mutation_types_encountered.add("remove_transition")
        if pickle.dumps(mutator.fsm.transitions) != original_transitions:
            mutation_types_encountered.add("modify_transition")
            
    assert mutation_types_encountered == expected_mutations, f"Missing mutation types: {expected_mutations - mutation_types_encountered}"

def test_create_mutated_fsm(mutated_fsm): #POSSIBLE TODO 
    mutated_fsm.draw("mutated.png")
    with open("mutated.pkl", "wb") as f:
        pickle.dump(mutated_fsm, f)
    assert isinstance(mutated_fsm, FSMGenerator)
    assert os.path.exists("mutated.pkl")

def test_mutation_application(mutator, testing_fsm): #ensures a previously applied mutation is not then mutated back to the original fsm
    original_fsm = pickle.dumps(testing_fsm)
    mutator._mutate()
    assert mutator.mutations_applied
    assert pickle.dumps(mutator.fsm) != original_fsm
    
'''BAD TESTS TO FIX'''

def test_mutation_preserves_connectivity(mutator): #TODO

    assert True

def test_mutated_fsm_determinism(mutator): #TODO

    assert True

'''END OF BAD TESTS'''

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

# create_mutated_fsm() # done ?

# _mutate() # done

# _add_state() # done

# _remove_state() # done

# _change_trigger_output() # done ? TODO

# _get_num_transitions_exclude_loops() ? TODO

# _change_trans_dest() # done ? TODO

# _check determinism() # tested elsewhere TODO

# _check connectivity() # tested elsewhere TODO

    # dfs() # tested elsewhere

# get_machine_properties() # only prints previous 2 function outputs
