import pytest
import collections
import random

from fsm_gen.generator import FSMGenerator



# Test that the generator creates a FSM and its states and transition numbers are correct
def test_fsm_creation():
    fsm = FSMGenerator(num_states=4, num_inputs=3)
    assert len(fsm.states) == 4
    assert len(fsm.events) == 3
    assert len(fsm.transitions) > 0
    assert fsm.states[0] == "S0"

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
    

# Test that ensures the FSM is connected
def test_fsm_connected():
    fsm = FSMGenerator(num_states=6, num_inputs=4)
    assert is_connected(fsm)

# Test that there's no duplicate transitions
def test_no_duplicate_transitions():
    fsm = FSMGenerator(num_states=6, num_inputs=4)
    transitions = [(t['source'], t['dest'], t['trigger']) for t in fsm.transitions]
    assert len(transitions) == len(set(transitions))

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

# Test 




### tests to do ###

## generator ##
# ensure connectivity # DONE
# ensure minimalism # DONE 
# ensure determinism # DONE
# ensure no duplicate transitions/states # DONE

## all generator functions ## 

# try_generate_connected_machine()

# generate_transitions()

# is_reachable_from()

# _get_triggers()

# _add_leftover_transitions()

# ensure_connected_machine()

# _find_1_equivalent()

# _get_dest_from_trigger()

# _get_transitions()

# _find_equivalent_states()

# _make_minimal()

# _cleanup_transitions()

# save()

# draw()

# apply_input_sequence()



################  STRESS TESTING  ################
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
def test_fsm_creation_large():
    fsm = FSMGenerator(num_states=50, num_inputs=10)
    assert len(fsm.states) == 50
    assert len(fsm.events) == 10
    assert len(fsm.transitions) > 0

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

    
