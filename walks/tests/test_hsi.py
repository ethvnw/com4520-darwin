import pytest

from fsm_gen.generator import FSMGenerator
from walks.hsi import HSI

@pytest.fixture
def fsm():
    """ A FSM for testing """
    return FSMGenerator(num_states=6, num_inputs=4)

@pytest.fixture
def hsi(fsm):
    """ A HSI for testing """
    return HSI(fsm)

def test_find_shortest_path(hsi):
    """ Ensure a valid list is returned """
    fsm = hsi.fsm
    state = fsm.states[-1] # the last state
    path = hsi._find_shortest_path(state) # the shortest path to the last state
    assert isinstance(path, list) # the path should be a list
    assert len(path) > 0 # the path should not be empty
    assert all(isinstance(event, str) for event in path) # all elements should be strings


def test_generate_state_cover(hsi):
    """ Ensure a valid dict is returned """
    state_cover = hsi._generate_state_cover()
    assert isinstance(state_cover, dict) # the state cover should be a dict
    assert len(state_cover) > 0 # the state cover should not be empty
    for path in state_cover.values():
        assert isinstance(path, list) # all values should be lists
        assert all(isinstance(event, str) for event in path)  # all elements should be strings


def test_generate_transition_cover(hsi):
    """ Ensure a valid non-empty set is returned """
    transition_cover = hsi._generate_transition_cover()
    assert isinstance(transition_cover, set) # the transition cover should be a set
    assert len(transition_cover) > 0 # the transition cover should not be empty
    assert all(isinstance(seq, str) for seq in transition_cover) # all elements should be strings


def test_compute_w_set(hsi):
    """ Checks if the W set differentiates states  """




def test_compute_hsi_sets(hsi):
    """ Checks if the HSI sets are computed correctly """
