import pytest

from fsm_gen.generator import FSMGenerator
from fsm_gen.machine import Machine
#from walks.hsi import hsi

from walks.hsi import (
    _find_shortest_path,
    _generate_state_cover,
    _generate_transition_cover,
    #_compute_w_set,
    generate_harmonised_state_identifiers,
    #_compute_h_sets,
    generate_HSI_suite
)

@pytest.fixture
def fsm():
    """A simple FSM for testing purposes"""
    fsm = FSMGenerator(num_states=3, num_inputs=2, num_outputs=2)
    
    # Manually override states, events, and transitions
    fsm.states = ['S0', 'S1', 'S2']
    fsm.events = ['a', 'b']
    fsm.transitions = [
        {'source': 'S0', 'trigger': 'a / x', 'dest': 'S1'},
        {'source': 'S1', 'trigger': 'b / y', 'dest': 'S2'},
        {'source': 'S2', 'trigger': 'a / z', 'dest': 'S0'},
    ]
    
    # Ensure the FSM machine instance is recreated with these values
    fsm.machine = fsm.machine = Machine(
        states=fsm.states,
        initial=fsm.states[0],
        graph_engine='pygraphviz',
        auto_transitions=False,
        transitions=fsm.transitions
    )

    return fsm



### IF ALREADY ON STATE THEN SHORTEST PATH IS EMPTY ####
### FIX IN CODE ###
def test_find_shortest_path(fsm):
    """ Ensure a valid list is returned and the path is correct """
    # making sure the shortest path is returned
    assert _find_shortest_path(fsm, 'S2') == ['a', 'b'] 
    assert _find_shortest_path(fsm, 'S1') == ['a'] 
    assert _find_shortest_path(fsm, 'S0') == [] 
    path = _find_shortest_path(fsm, 'S2')
    # checking structure of path
    assert isinstance(path, list)
    assert all(isinstance(event, str) for event in path)


def test_generate_state_cover(fsm):
    """ Ensure a valid structure and state cover is returned """
    state_cover = _generate_state_cover(fsm)
    assert isinstance(state_cover, dict) # the state cover should be a dict
    assert len(state_cover) > 0 # the state cover should not be empty
    for path in state_cover.values():
        assert isinstance(path, list) # all values should be lists
        assert all(isinstance(event, str) for event in path)  # all elements should be strings
    # make sure a correct state cover is returned
    assert state_cover == {
        'S0': [],
        'S1': ['a'],
        'S2': ['a', 'b']
    }


def test_generate_transition_cover(fsm):
    """ Ensure a valid non-empty set is returned """
    transition_cover = _generate_transition_cover(fsm)
    # make sure structure is correct
    assert isinstance(transition_cover, set) # the transition cover should be a set
    assert len(transition_cover) > 0 # the transition cover should not be empty
    assert all(isinstance(seq, str) for seq in transition_cover) # all elements should be strings
    # ensuring the correct transition cover is returned
    assert transition_cover == {'a', 'ab', 'aba'}


def test_compute_h_sets(fsm):
    """ Checks if the H sets are correctly returned """
    h_sets = generate_harmonised_state_identifiers(fsm)
    # make sure the structure is correct
    assert isinstance(h_sets, dict) 
    assert len(h_sets) > 0 
    assert set(h_sets.keys()).issubset(fsm.states) # states
    for path in h_sets.values():
        assert isinstance(path, set) 
        assert all(isinstance(event, str) for event in path)


def test_generate_HSI_suite(fsm):
    identifiers = generate_harmonised_state_identifiers(fsm)
    hsi_suite = generate_HSI_suite(fsm, identifiers)
    assert isinstance(hsi_suite, dict)
    assert len(hsi_suite) > 0
    for seq, output in hsi_suite.items():
        assert isinstance(seq, str)
