import pytest
import collections
import random
import pickle
import os
from fsm_gen.generator import FSMGenerator
from fsm_gen.machine import Machine
from fsm_gen.mutator import Mutator

@pytest.fixture
def sample_fsm():
    fsm = FSMGenerator(num_states=5, num_inputs=3)
    fsm.draw("original.png")
    return fsm

@pytest.fixture
def mutator(sample_fsm):
    return Mutator(sample_fsm)

@pytest.fixture
def mutated_fsm(mutator):
    mutator._mutate()
    return mutator.fsm

def test_create_mutated_fsm(mutated_fsm):
    mutated_fsm.draw("mutated.png")
    with open("mutated.pkl", "wb") as f:
        pickle.dump(mutated_fsm, f)
    assert isinstance(mutated_fsm, FSMGenerator)
    assert os.path.exists("mutated.pkl")

def test_mutation_application(mutator, sample_fsm):
    original_fsm = pickle.dumps(sample_fsm)
    mutator._mutate()
    assert mutator.mutations_applied
    assert pickle.dumps(mutator.fsm) != original_fsm
    
'''BAD TESTS TO FIX'''

def test_fsm_connectivity(mutator):
    mutator._mutate()
    assert mutator._check_connectivity()

def test_check_connectivity(sample_fsm):
    assert sample_fsm.ensure_connected_machine()

def test_mutation_preserves_connectivity(mutator):
    mutator._mutate()
    assert mutator.fsm.ensure_connected_machine()

def test_fsm_determinism(mutator):
    mutator._mutate()
    assert isinstance(mutator._check_determinism(), bool)
    
'''END OF BAD TESTS'''

def test_pickle_creation(mutated_fsm):
    with open("mutated.pkl", "wb") as f:
        pickle.dump(mutated_fsm, f)
    with open("mutated.pkl", "rb") as f:
        loaded_fsm = pickle.load(f)
    assert isinstance(loaded_fsm, FSMGenerator)

def test_mutation_effects():
    """Test if all types of mutations are applied by running multiple mutations on fresh FSM instances."""
    mutation_types_encountered = set()
    expected_mutations = {"add_state", "remove_state", "add_transition", "remove_transition", "modify_transition"}
    for _ in range(20):  # Run multiple mutations to cover all types
        fsm = FSMGenerator(num_states=5, num_inputs=3)  # Create a fresh FSM
        mutator = Mutator(fsm)  # Create a new Mutator instance
        initial_state_count = len(fsm.states)
        initial_transition_count = len(fsm.transitions)
        original_transitions = pickle.dumps(fsm.transitions)
        mutator._mutate()
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
