import pytest
import collections
import random
import pickle
import os

from fsm_gen.generator import FSMGenerator

@pytest.fixture
def fsm():
    return FSMGenerator(num_states=6, num_inputs=4)

# Test that the generator creates a FSM and its states and transition numbers are correct
def test_fsm_creation(fsm):
    #fsm = FSMGenerator(num_states=4, num_inputs=3)
    assert len(fsm.states) == 6
    assert len(fsm.events) == 4
    assert len(fsm.transitions) == len(fsm.states) * len(fsm.events) # each state has a transition for each event
    assert fsm.states[0] == "S0"

def test_fsm_zero_states():
    """ Test that the generator raises an error if the number of states is zero """
    with pytest.raises(IndexError):
        FSMGenerator(num_states=0, num_inputs=3)

def test_fsm_zero_inputs():
    """ Test that the generator raises an error if the number of inputs is zero """
    with pytest.raises(ValueError):
        FSMGenerator(num_states=4, num_inputs=0)

def test_fsm_negative_states():
    """ Test that the generator raises an error if the number of states is negative """
    with pytest.raises(IndexError):
        FSMGenerator(num_states=-1, num_inputs=3)

def test_fsm_negative_inputs():
    """ Test that the generator raises an error if the number of inputs is negative """
    with pytest.raises(ValueError):
        FSMGenerator(num_states=4, num_inputs=-1)

def test_fsm_single_state():
    """ Test that the generator creates a FSM with a single state """
    fsm = FSMGenerator(num_states=1, num_inputs=3)
    assert len(fsm.states) == 1
    assert len(fsm.events) == 3
    assert len(fsm.transitions) == len(fsm.states) * len(fsm.events)
    assert fsm.states[0] == "S0"

# def test_fsm_single_input():
#     """ Test that the generator creates a FSM with a single input """
#     fsm = FSMGenerator(num_states=2, num_inputs=1)
#     assert len(fsm.states) == 2
#     assert len(fsm.events) == 1
#     assert len(fsm.transitions) == len(fsm.states) * len(fsm.events)
#     assert fsm.events[0] == "A"
    

# Test that transitions are generated correctly
def test_generate_transitions():
    fsm = FSMGenerator(num_states=4, num_inputs=3)
    assert isinstance(fsm.transitions, list)
    assert len(fsm.transitions) > 0
    for transition in fsm.transitions:
        assert "trigger" in transition
        assert "source" in transition
        assert "dest" in transition
        assert transition["source"] in fsm.states
        assert transition["dest"] in fsm.states

# Test the function to check if a state is reachable from another
def test_is_reachable_from():
    fsm = FSMGenerator(num_states=4, num_inputs=3)
    for state in fsm.states:
        for target in fsm.states:
            assert fsm._is_reachable_from(state, target) or (state == target)
    
# Check if the FSM is connected
def is_connected(fsm):
    def dfs(start_state):
        visited = set()
        stack = [start_state]
        while stack:
            state = stack.pop()
            if state not in visited:
                visited.add(state)
                for transition in fsm.transitions:
                    if transition['source'] == state:
                        stack.append(transition['dest'])
        return visited

    all_states = set(fsm.states)
    for state in fsm.states:
        if dfs(state) != all_states:
            return False
        
    return True

# Test that ensures the FSM is connected
def test_fsm_connected():
    fsm = FSMGenerator(num_states=6, num_inputs=4)
    assert is_connected(fsm)

# Test that there's no duplicate transitions
def test_no_duplicate_transitions():
    fsm = FSMGenerator(num_states=6, num_inputs=4)
    transitions = [(t['source'], t['dest'], t['trigger']) for t in fsm.transitions]
    assert len(transitions) == len(set(transitions))


# Test if the FSM is deterministic
def is_deterministic(fsm):
    events = collections.Counter(fsm.events)

    for state in fsm.states:
        transitions = [t for t in fsm.transitions if t["source"] == state]
        triggers = [t["trigger"].split(' / ')[0] for t in transitions]

        if collections.Counter(triggers) != events:
            return False
        
    return True

# Test that the FSM is deterministic
def test_fsm_deterministic():
    fsm = FSMGenerator(num_states=5, num_inputs=3)
    assert is_deterministic(fsm)

# Test that the FSM is minimal
def test_fsm_minimal():
    fsm = FSMGenerator(num_states=7, num_inputs=4)
    initial_state_count = len(fsm.states)
    fsm._make_minimal()
    assert is_connected(fsm)
    assert is_deterministic(fsm)
    assert len(fsm.states) <= initial_state_count

# Test getting triggers from a state
def test_get_triggers():
    fsm = FSMGenerator(num_states=5, num_inputs=3)
    state = fsm.states[0]
    triggers = fsm._get_triggers(state)
    assert isinstance(triggers, list)

# Test adding tranaitions that are missing to make the FSM complete
def test_add_leftover_transitions():
    fsm = FSMGenerator(num_states=6, num_inputs=4)
    initial_transitions = len(fsm.transitions)
    fsm._add_leftover_transitions()
    assert len(fsm.transitions) >= initial_transitions

# Test finding 1-equivalent states
def test_find_1_equivalent():
    fsm = FSMGenerator(num_states=6, num_inputs=4)
    equivalence_sets = fsm._find_1_equivalent()
    assert isinstance(equivalence_sets, dict)
    for key, value in equivalence_sets.items():
        assert isinstance(value, set)

# Test getting the destination state from a trigger
def test_get_dest_from_trigger():
    fsm = FSMGenerator(num_states=6, num_inputs=4)
    state = fsm.states[0]
    trigger = fsm._get_triggers(state)[0]
    dest = fsm._get_dest_from_trigger(state, trigger)
    assert dest in fsm.states or dest is None

# Test getting all transitions from a state
def test_get_transitions():
    fsm = FSMGenerator(num_states=6, num_inputs=4)
    state = fsm.states[0]
    transitions = fsm._get_transitions(source=state)
    assert isinstance(transitions, list)
    for transition in transitions:
        assert "trigger" in transition
        assert "source" in transition
        assert "dest" in transition

# Test finding equivalent states
def test_find_equivalent_states():
    fsm = FSMGenerator(num_states=6, num_inputs=4)
    equivalent_states = fsm._find_equivalent_states()
    assert isinstance(equivalent_states, list)
    for eqviv_set in equivalent_states:
        assert isinstance(eqviv_set, set)

# Test removing duplicate transitions
def test_cleanup_transitions():
    fsm = FSMGenerator(num_states=6, num_inputs=4)
    initial_transitions = len(fsm.transitions)
    fsm._cleanup_transitions()
    assert len(fsm.transitions) <= initial_transitions

# Test saving the FSM and loading it
def test_save(tmp_path):
    fsm = FSMGenerator(num_states=3, num_inputs=2)
    file_path = tmp_path / "fsm.pkl"

    fsm.save(str(file_path))
    loaded_fsm = pickle.load(open(file_path, "rb"))

    assert loaded_fsm.states == fsm.states
    assert loaded_fsm.events == fsm.events
    assert loaded_fsm.transitions == fsm.transitions


# Test applying an input sequence to the FSM
def test_apply_input_sequence():
    fsm = FSMGenerator(num_states=4, num_inputs=3)
    state = fsm.states[0]
    sequence = "".join(fsm.events)  # Using all possible events

    final_state, output_seq = fsm.apply_input_sequence(state, sequence)

    assert final_state in fsm.states
    assert isinstance(output_seq, tuple)
    assert len(output_seq) == len(sequence)



################  STRESS TESTING  ################

# Test FSM generation with different sizes.
@pytest.mark.parametrize("num_states, num_inputs", [(3, 2), (5, 3), (10, 4)])
def test_fsm_different_sizes(num_states, num_inputs):
    fsm = FSMGenerator(num_states=num_states, num_inputs=num_inputs)

    assert len(fsm.states) == num_states
    assert len(fsm.events) == num_inputs
    assert len(fsm.transitions) > 0

# # run test on 500 random FSMs
# tests_failed = []
# for i in range(1000):
#     fsm = FSMGenerator(num_states=10, num_inputs=2)
#     try:
#         assert is_connected(fsm)
#         assert is_deterministic(fsm)
#     except AssertionError:
#         tests_failed.append(i)
#         print(f"{i}: Connected: {is_connected(fsm)}")
#         print(f"{i}: Deterministic: {is_deterministic(fsm)}")
#         fsm.draw(f"error_{i}.png")

# Test fsm for 50 states and 10 inputs
# def test_fsm_creation_large():
#     fsm = FSMGenerator(num_states=50, num_inputs=10)
#     assert len(fsm.states) == 50
#     assert len(fsm.events) == 10
#     assert len(fsm.transitions) > 0

# Takes ages so comment out
# Test fsm for 80 states and 30 inputs
# def test_fsm_creation_large():
#     fsm = FSMGenerator(num_states=80, num_inputs=30)
#     assert len(fsm.states) == 80
#     assert len(fsm.events) == 30
#     assert len(fsm.transitions) > 0

# Takes ages so comment out
# Test fsm for 100 states and 50 inputs
# def test_fsm_creation_large():
#     fsm = FSMGenerator(num_states=100, num_inputs=50)
#     assert len(fsm.states) == 100
#     assert len(fsm.events) == 50
#     assert len(fsm.transitions) > 0

    
