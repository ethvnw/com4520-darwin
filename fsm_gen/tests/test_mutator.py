import pytest
import collections
import random
import pickle
import os
import re
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

def test_add_state():
    fsm = FSMGenerator(num_states=5, num_inputs=3)
    mutator = Mutator(fsm)
    initial_state_count = len(fsm.states)
    mutator._add_state()
    assert len(mutator.fsm.states) > initial_state_count

def test_remove_state():
    fsm = FSMGenerator(num_states=5, num_inputs=3)
    mutator = Mutator(fsm)
    initial_state_count = len(fsm.states)
    mutator._remove_state()
    assert len(mutator.fsm.states) < initial_state_count
    
def test_change_trigger_output():
    fsm = FSMGenerator(num_states=5, num_inputs=3)
    mutator = Mutator(fsm)
    initial_trigger = []
    initial_source = []
    initial_dest = []
    found = False
    for i in range(0,len(fsm.transitions)):
        initial_trigger.append(fsm.transitions[i]["trigger"])
        initial_source.append(fsm.transitions[i]["source"])
        initial_dest.append(fsm.transitions[i]["dest"])
    print(fsm.transitions)
    mutator._change_trigger_output()
    print(fsm.transitions)
    for i in range(0,len(fsm.transitions)):
        for j in range(0,len(fsm.transitions)):
            if fsm.transitions[i]["dest"] == initial_dest[j] and fsm.transitions[i]["source"] == initial_source[j]:
                if fsm.transitions[i]["trigger"] != initial_trigger[j]:
                    found = True
                    break
        if found == True:
            break
    assert found
    
def test_change_trans_dest():
    fsm = FSMGenerator(num_states=5, num_inputs=3)
    mutator = Mutator(fsm)
    initial_trigger = []
    initial_source = []
    initial_dest = []
    found = False
    for i in range(0,len(fsm.transitions)):
        initial_trigger.append(fsm.transitions[i]["trigger"])
        initial_source.append(fsm.transitions[i]["source"])
        initial_dest.append(fsm.transitions[i]["dest"])
    print(fsm.transitions)
    mutator._change_trans_dest()
    print(fsm.transitions)
    for i in range(0,len(fsm.transitions)):
        for j in range(0,len(fsm.transitions)):
            if fsm.transitions[i]["trigger"] == initial_trigger[j] and fsm.transitions[i]["source"] == initial_source[j]:
                if fsm.transitions[i]["dest"] != initial_dest[j]:
                    found = True
                    break
        if found == True:
            break
    assert found

# TODO discuss this
'''
def test_mutation_effects(): # had 1 error in 1000 test runs
    """Test if all types of mutations are applied by running multiple mutations on fresh FSM instances."""
    mutation_types_encountered = set()
    expected_mutations = {"add_state", "remove_state", "change_trigger_output", "change_transition_destination"} ### STILL TO FIX
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
'''

def test_create_mutated_fsm(mutated_fsm): #POSSIBLE TODO 
    mutated_fsm.draw("mutated.png")
    with open("mutated.pkl", "wb") as f:
        pickle.dump(mutated_fsm, f)
    assert isinstance(mutated_fsm, FSMGenerator)
    assert os.path.exists("mutated.pkl")

def test_mutation_application(mutator, testing_fsm): #ensures a previously applied mutation is not then mutated back to the original fsm
    original_fsm = pickle.dumps(testing_fsm)
    mutator.create_mutated_fsm()
    assert mutator.mutations_applied
    assert pickle.dumps(mutator.fsm) != original_fsm
    
'''BAD TESTS TO FIX'''

def test_mutation_preserves_connectivity(mutator): #TODO

    assert True

def test_mutated_fsm_determinism(mutator): #TODO

    assert True
    
'''END OF BAD TESTS'''

# TODO Discuss this too
''' Confused by how to test this'''
'''
def test_get_machine_properties(testing_fsm):
    fsm = FSMGenerator(num_states=5, num_inputs=3)
    fsm._check_connectivity() = True
    fsm._check_determinism() = True
    assert Mutator.get_machine_properties(fsm) == (f"\nConnected: True, Deterministic: True")'''

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

# _change_trigger_output() # done ? TODO

# _change_trans_dest() # done ? TODO

# _get_num_transitions_exclude_loops() #  TODO

# _check determinism() #  TODO

# _check connectivity() # TODO

# get_machine_properties() # TODO
